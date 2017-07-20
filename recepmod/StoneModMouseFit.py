import pandas as pd
import numpy as np
from memoize import memoize
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
    y = data['Effectiveness'].as_matrix()

    # Log transform to keep ratios
    X = X.apply(np.log10).replace(-np.inf, -3).as_matrix()

    # Run crossvalidation predictions at the same time
    data['DirectPredict'], dp, data['CrossPredict'], cp, _ = LOOpredict(regFunc(logg=False),
                                                                        X, y)

    return (dp, cp, data)


@memoize
def caller(**kwargs):
    from .StoneNRecep import StoneN
    return StoneN(**kwargs).getActivity([1, -1, 1, 1])


def CALCapply(row):
    from .StoneHelper import getMedianKx

    KaFull = [row.FcgRI + 1.0E-6, row.FcgRIIB, row.FcgRIII, row.FcgRIV]

    kwarg = {'Ka': KaFull, 'Kx': getMedianKx(), 'gnu': row.v, 'L0': row.L0}

    row['ncMO'] = caller(logR=[3.28, 4.17, 3.81, 4.84], **kwarg)  # non-classic MO
    row['NE'] = caller(logR=[1.96, 3.08, 3.88, 4.07], **kwarg)  # neutrophils
    row['cMO'] = caller(logR=[3.49, 4.13, 4.18, 3.46], **kwarg)  # classic MO
    row['NKs'] = caller(logR=[1.54, 3.21, 3.23, 2.23], **kwarg)  # NK
    row['EO'] = caller(logR=[1.96, 4.32, 4.22, 2.60], **kwarg)  # Eosino

    return row


cellpops = ['cMO', 'NE', 'ncMO', 'NKs', 'EO']


def modelPrepAffinity(v, L0):
    """ Setup data for model. """
    data = StoneModelMouse().NimmerjahnEffectTableAffinities()
    data['v'] = v
    data['L0'] = L0

    data = data.apply(CALCapply, axis=1)

    data.loc['None', :] = 0.0

    # Assign independent variables and dependent variable
    X = data[cellpops].as_matrix()
    y = data['Effectiveness'].as_matrix()

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


@memoize
def InVivoPredict(inn=[5, 1E-9]):
    """ Cross validate KnockdownLasso by using a pair of rows as test set """
    pd.set_option('expand_frame_repr', False)

    inn = np.squeeze(inn)

    # Collect data
    X, y, tbl = modelPrepAffinity(v=inn[0], L0=inn[1])

    tbl['DPredict'], dperf, tbl['CPredict'], cperf, model = LOOpredict(regFunc(), X, y)

    tbl['Error'] = np.square(tbl.CPredict - y)

    print('InVivoPredict direct r2: ' + str(round(dperf, 3)))
    print('InVivoPredict crossval r2: ' + str(round(cperf, 3)))

    for ii, item in enumerate(cellpops):
        tbl[item + 'eff'] = tbl[item] * np.power(10, model.res.x[ii])

    return (dperf, cperf, tbl, model)


def InVivoPredictMinusComponents():
    ''' '''
    def crossValF(table):
        return LOOpredict(regFunc(),
                          table.drop('Effectiveness', axis=1),
                          table['Effectiveness'])[3]

    _, cperf, data, _ = InVivoPredict()

    data = data[['Effectiveness'] + cellpops]

    table = pd.DataFrame(cperf, columns=['CrossVal'], index=['Full Model'])

    for _, items in enumerate(cellpops):
        table.loc['No ' + items, :] = crossValF(data.drop(items, axis=1))

    return table
