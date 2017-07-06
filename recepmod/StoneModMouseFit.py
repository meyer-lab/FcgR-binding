import pandas as pd
import numpy as np
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


def CALCapply(row):
    from .StoneModel import StoneMod
    from .StoneNRecep import StoneN
    from .StoneHelper import getMedianKx

    KaFull = [row.FcgRI + 0.00001, row.FcgRIIB, row.FcgRIII, row.FcgRIV]

    if 'exprI' in row:
        logRtwo = [row.exprI, row.exprIIB, row.exprIII, row.exprIV]

        row['NK'] = StoneN(logR=logRtwo, Ka=KaFull, Kx=getMedianKx(),
                           gnu=row.v, L0=row.L0).getActivity([1, -1, 1, 1])
    else:
        row['NK'] = StoneMod(logR=2.0, Ka=row.FcgRIII, v=row.v,
                             Kx=getMedianKx() * row.FcgRIII, L0=row.L0)[2] * 1.0E6

    row['DC'] = StoneN(logR=[2, 3, 2, 2], Ka=KaFull, Kx=getMedianKx(),
                       gnu=row.v, L0=row.L0).getActivity([1, -1, 1, 1])

    return row


def modelPrepAffinity(v=5, L0=1E-12, exprV=None):

    data = StoneModelMouse().NimmerjahnEffectTableAffinities()
    data['v'] = v
    data['L0'] = L0

    if exprV is not None:
        data['exprI'] = exprV[0]
        data['exprIIB'] = exprV[1]
        data['exprIII'] = exprV[2]
        data['exprIV'] = exprV[3]

    data = data.apply(CALCapply, axis=1)

    data.loc['None', :] = 0.0

    # Assign independent variables and dependent variable
    X = data[['NK', 'DC']].as_matrix()
    y = data['Effectiveness'].as_matrix()

    return (X, y, data)


def LOOpredict(lr, X, y):
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


def InVivoPredict(inn=[5, 1E-12], exprV=None):
    """ Cross validate KnockdownLasso by using a pair of rows as test set """
    pd.set_option('expand_frame_repr', False)

    inn = np.squeeze(inn)

    # Collect data
    X, y, tbl = modelPrepAffinity(v=inn[0], L0=inn[1], exprV=exprV)

    tbl['DPredict'], dperf, tbl['CPredict'], cperf, model = LOOpredict(regFunc(), X, y)

    XX = np.power(10, model.res.x)

    tbl['NKeff'] = tbl.NK * XX[0]
    tbl['DCeff'] = tbl.DC * XX[1]
    tbl['NKfrac'] = tbl.NKeff / (tbl.DCeff + tbl.NKeff)
    tbl['Error'] = np.square(tbl.CPredict - y)

    return (dperf, cperf, tbl, model)


def InVivoPredictMinusComponents():
    ''' '''
    def crossValF(table):
        return LOOpredict(regFunc(),
                          table.drop('Effectiveness', axis=1),
                          table['Effectiveness'])[3]

    _, cperf, data, _ = InVivoPredict()

    data = data[['Effectiveness', 'NK', 'DC']]

    table = pd.DataFrame(cperf, columns=['CrossVal'], index=['Full Model'])

    table.loc['No NK', :] = crossValF(data.drop('NK', axis=1))
    table.loc['No DC', :] = crossValF(data.drop('DC', axis=1))

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

        ub = np.full((X.shape[1], ), 6.0)

        res = differential_evolution(self.errF, bounds=list(zip(-ub, ub)),
                                     polish=True, disp=False)

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
