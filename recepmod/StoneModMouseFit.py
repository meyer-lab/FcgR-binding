import pandas as pd
import numpy as np
from memoize import memoize
from sklearn.base import BaseEstimator
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


cellpops = ['cMO', 'EO', 'NE', 'ncMO']


def modelPrepAffinity(v=5, L0=1E-12):

    data = StoneModelMouse().NimmerjahnEffectTableAffinities()
    data['v'] = v
    data['L0'] = L0

    data = data.apply(CALCapply, axis=1)

    data.loc['None', :] = 0.0

    # Assign independent variables and dependent variable
    X = data[cellpops].as_matrix()
    y = data['Effectiveness'].as_matrix()

    return (X, y, data)


def LOOpredict(lr, X, y, cPred=True):
    from sklearn.model_selection import cross_val_predict
    from sklearn.metrics import r2_score

    # Do LOO prediction
    crossPred = cross_val_predict(lr, X, y, cv=len(y))

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

    XX = np.power(10, model.res.x)

    for ii in range(len(cellpops)):
        tbl[cellpops[ii] + 'eff'] = tbl[cellpops[ii]] * XX[ii]

    tbl['Error'] = np.square(tbl.CPredict - y)

    print('InVivoPredict direct r2: ' + str(round(dperf, 3)))
    print('InVivoPredict crossval r2: ' + str(round(cperf, 3)))

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

    for ii in range(len(cellpops)):
        table.loc['No ' + cellpops[ii], :] = crossValF(data.drop(cellpops[ii], axis=1))

    return table


class regFunc(BaseEstimator):
    """ Class to handle regression with saturating effect. """

    def __init__(self, logg=True):
        self.logg = logg
        self.res, self.trainX, self.trainy = None, None, None

    def fit(self, X, y):
        """ Fit the X-y relationship. Return nothing. """
        from scipy.optimize import least_squares, differential_evolution

        self.trainX, self.trainy = X, y

        ub = np.full((X.shape[1], ), 12.0)

        res = differential_evolution(self.errF, bounds=list(zip(-ub, ub)), disp=False)

        self.res = least_squares(self.diffF, x0=res.x, jac='3-point', bounds=(-ub, ub))

    def diffF(self, p):
        return self.trainy - self.predict(p=p)

    def errF(self, p):
        return np.sum(np.square(self.trainy - self.predict(p=p))) / 2.0

    def predict(self, X=None, p=None):
        """
        Output prediction from parameter set. Use internal X if none given.
        """
        from scipy.special import expit

        if p is None:
            p = self.res.x

        if self.logg is True:
            p = np.power(10, p)

        if X is None:
            X = self.trainX

        return 2.0 * (expit(np.dot(X, p)) - 0.5)
