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

    # Run regression with our setup
    lr = regFunc()
    lr.logg = False

    data = StoneModelMouse().NimmerjahnEffectTableAffinities()
    data['ActMax'] = data.apply(lambda x: max(x.FcgRI,
                                              x.FcgRIII,
                                              x.FcgRIV), axis=1)

    X = data[['ActMax', 'FcgRIIB']]
    y = data['Effectiveness']

    # Log transform to keep ratios
    X = X.apply(np.log10).replace(-np.inf, -3)

    # Run crossvalidation predictions at the same time
    data['DirectPredict'], dperf, data['CrossPredict'], cperf, lr = LOOpredict(lr, X, y)

    return (dperf, cperf, data)


def CALCapply(row):
    import re
    from .StoneModel import StoneMod
    from .StoneNRecep import StoneN
    from .StoneHelper import getMedianKx

    KaFull = [row.FcgRI + 0.00001, row.FcgRIIB, row.FcgRIII, row.FcgRIV]

    row['NK'] = StoneMod(logR=2.0, Ka=row.FcgRIII, v=row.v,
                         Kx=getMedianKx() * row.FcgRIII, L0=row.L0)[2]

    row['DC'] = StoneN(logR=[2, 3, 2, 2], Ka=KaFull, Kx=getMedianKx(),
                       gnu=row.v, L0=row.L0).getActivity([1, -1, 1, 1])

    row['2B-KO'] = not re.search('FcgRIIB-', row.name) is None

    return row

# TODO: Change all regression metrics to R2


def modelPrepAffinity(v=5, L0=1E-12):

    data = StoneModelMouse().NimmerjahnEffectTableAffinities()
    data['v'] = v
    data['L0'] = L0

    data = data.apply(CALCapply, axis=1)

    data.loc['None', :] = 0.0

    data = data.iloc[:, 4:]

    # Assign independent variables and dependent variable
    X = data[['NK', 'DC', '2B-KO']].as_matrix()
    y = data['Effectiveness'].as_matrix()

    return (X, y, data)


def LOOpredict(lr, X, y):
    from sklearn.model_selection import cross_val_predict
    from sklearn.metrics import r2_score

    # Do LOO prediction
    crossPred = cross_val_predict(lr, X, y, cv=X.shape[0])

    # How well did we do on crossvalidation?
    crossval_perf = r2_score(y, crossPred)

    # Do direct regression
    lr.fit(X, y)

    # Do direct prediction
    dirPred = lr.predict(X)

    # How well did we do on direct?
    direct_perf = r2_score(y, dirPred)

    return (dirPred, direct_perf, crossPred, crossval_perf, lr)


def InVivoPredict(inn=[5, 1E-12]):
    """ Cross validate KnockdownLasso by using a pair of rows as test set """
    pd.set_option('expand_frame_repr', False)

    inn = np.squeeze(inn)

    # Collect data
    try:
        X, y, tbl = modelPrepAffinity(v=inn[0], L0=inn[1])
    except RuntimeError:
        return np.nan

    tbl['DPredict'], dperf, tbl[
        'CPredict'], cperf, model = LOOpredict(regFunc(), X, y)

    XX = np.power(10, model.res.x)

    tbl['NKeff'] = tbl.NK * XX[0]
    tbl['DCeff'] = tbl.DC * XX[1]
    tbl['2Beff'] = tbl['2B-KO'] * XX[2]
    tbl['NKfrac'] = tbl.NKeff / (tbl.DCeff + tbl.NKeff + tbl['2Beff'])
    tbl['Error'] = np.square(tbl.CPredict - y)

    print(cperf)

    return (dperf, cperf, tbl, model)


def InVivoPredictMinusComponents():
    ''' '''
    def crossValF(table):
        return LOOpredict(regFunc(),
                          table.drop('Effectiveness', axis=1),
                          table['Effectiveness'])[2]

    _, cperf, data, _ = InVivoPredict()

    data = data[['Effectiveness', 'NK', 'DC', '2B-KO']]

    table = pd.DataFrame(cperf, columns=['CrossVal'], index=['Full Model'])

    table.loc['No 2B', :] = crossValF(data.drop('2B-KO', axis=1))
    table.loc['No NK', :] = crossValF(data.drop('NK', axis=1))
    table.loc['No DC', :] = crossValF(data.drop('DC', axis=1))

    return table


class regFunc(BaseEstimator):
    """ Class to handle regression with saturating effect. """

    def __init__(self):
        self.logg = True
        self.res = None
        self.trainX = None
        self.trainy = None

    def fit(self, X, y):
        """ Fit the X-y relationship. Return nothing. """
        from scipy.optimize import least_squares, differential_evolution

        self.trainX, self.trainy = X, y

        lb = np.full((X.shape[1], ), -10.0, dtype=np.float64)
        ub = np.full((X.shape[1], ), 10.0, dtype=np.float64)

        self.res = differential_evolution(self.errF, bounds=list(zip(lb, ub)),
                                          popsize=30, polish=True)
        self.res.cost = self.res.fun
        x0 = self.res.x

        for ii in range(5):
            resC = least_squares(self.diffF, x0=x0,
                                 jac='3-point', bounds=(lb, ub))

            if resC.cost < self.res.cost:
                self.res = resC

            x0 = np.random.uniform(lb, ub)

    def diffF(self, p):
        return self.trainy - self.predict(p=p)

    def errF(self, p):
        return np.sum(np.square(self.trainy - self.predict(p=p))) / 2.0

    def predict(self, X=None, p=None):
        """
        Output prediction from parameter set. Use internal X if none given.
        """

        if p is None:
            p = self.res.x

        if self.logg is True:
            p = np.power(10, p)

        if X is None:
            X = self.trainX

        return np.tanh(np.dot(X, p))
