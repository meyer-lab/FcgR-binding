from collections import OrderedDict
import pandas as pd
import numpy as np
from .regFunc import regFunc
from .StoneModMouse import StoneModelMouse


def NimmerjahnPredictByAIratio():
    """ Predict in vivo efficacy using the AtoI ratio. """
    from sklearn.linear_model import LinearRegression

    lr = LinearRegression()
    table = StoneModelMouse().NimmerjahnEffectTableAffinities()
    table = table.loc[table.FcgRIIB > 0, :]
    table['AtoI'] = table.apply(lambda x: max(x.FcgRI,
                                              x.FcgRIII,
                                              x.FcgRIV) / x.FcgRIIB, axis=1)
    X = table[['AtoI']].apply(np.log10)
    y = table['Effectiveness']

    # Run predictions at the same time
    table['DirectPredict'], dperf, table['CrossPredict'], cperf, lr = LOOpredict(lr, X, y)

    return (dperf, cperf, table, lr.coef_, lr.intercept_)


def NimmerjahnPredictByAffinities():
    """
    This will run ordinary linear regression using just
    affinities of receptors.
    """

    data = StoneModelMouse().NimmerjahnEffectTableAffinities()
    data['ActMax'] = data.apply(lambda x: max(x.FcgRI,
                                              x.FcgRIII,
                                              x.FcgRIV), axis=1)

    X = data[['ActMax', 'FcgRIIB']]
    y = data['Effectiveness'].values

    # Log transform to keep ratios
    X = X.apply(np.log10).replace(-np.inf, -3).values

    # Run crossvalidation predictions at the same time
    data['DirectPredict'], dp, data['CrossPredict'], cp, _ = LOOpredict(regFunc(logg=False),
                                                                        X, y)

    return (dp, cp, data)


def caller(**kwargs):
    from .StoneNRecep import StoneN
    return StoneN(**kwargs).getActivity([1, -1, 1, 1])

exprDict = OrderedDict(zip(['ncMO', 'NE', 'cMO', 'NKs', 'EO'],
                           [[3.28, 4.17, 3.81, 4.84],
                            [1.96, 3.08, 3.88, 4.07],
                            [3.49, 4.13, 4.18, 3.46],
                            [1.54, 3.21, 3.23, 2.23],
                            [1.96, 4.32, 4.22, 2.60]]))


def CALCapply(row):
    from .StoneHelper import getMedianKx

    KaFull = [row.FcgRI + 1.0E-6, row.FcgRIIB, row.FcgRIII, row.FcgRIV]

    kwarg = {'Ka': KaFull, 'Kx': getMedianKx(), 'gnu': row.v, 'L0': row.L0}

    for key, item in exprDict.items():
        internalExpr = np.asarray(item)

        internalExpr[internalExpr < 3] = -8

        row[key] = caller(logR=internalExpr, **kwarg)  # get predictions

    return row


cellpops = list(exprDict.keys())


def modelPrepAffinity(v, L0):
    """ Setup data for model. """
    data = StoneModelMouse().NimmerjahnEffectTableAffinities()
    data['v'] = v
    data['L0'] = L0

    data = data.apply(CALCapply, axis=1)

    data.loc['None', :] = 0.0

    # Assign independent variables and dependent variable
    X = data[cellpops].values
    y = data['Effectiveness'].values

    return (X, y, data)


def LOOpredict(lr, X, y):
    from sklearn.model_selection import cross_val_predict
    from sklearn.metrics import r2_score

    # Do LOO prediction
    crossPred = cross_val_predict(lr, X, y, cv=len(y), n_jobs=-1)

    # How well did we do on crossvalidation?
    crossval_perf = r2_score(y, crossPred)

    # Do direct regression
    lr.fit(X, y)

    # Do direct prediction
    dirPred = lr.predict(X)

    # How well did we do on direct?
    direct_perf = r2_score(y, dirPred)

    return (dirPred, direct_perf, crossPred, crossval_perf, lr)


def InVivoPredict(inn=None):
    """ Cross validate KnockdownLasso by using a pair of rows as test set """
    if inn is None:
        inn = [5, 1E-9]

    # Collect data
    X, y, tbl = modelPrepAffinity(v=inn[0], L0=inn[1])

    tbl['DPredict'], dperf, tbl['CPredict'], cperf, model = LOOpredict(regFunc(), X, y)

    tbl['Error'] = np.square(tbl.CPredict - y)

    for ii, item in enumerate(cellpops):
        tbl[item + 'eff'] = tbl[item] * np.power(10, model.res.x[ii]) / model.scale.scale_[ii]

    return (dperf, cperf, tbl, model)


def InVivoPredictMinusComponents():
    ''' Predict in vivo conditions with one cell type left out. '''
    def crossValF(table):
        return LOOpredict(regFunc(),
                          table.drop('Effectiveness', axis=1),
                          table['Effectiveness'])[3]

    _, cperf, data, _ = InVivoPredict()

    data = data[['Effectiveness'] + cellpops]

    table = pd.DataFrame(cperf, columns=['CrossVal'], index=['Full Model'])

    for _, item in enumerate(cellpops):
        table.loc['No ' + item, :] = crossValF(data.drop(item, axis=1))

    return table
