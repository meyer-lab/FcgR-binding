import re
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import explained_variance_score
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
    # Do direct regression too
    lr.fit(X, y)
    table['DirectPredict'] = lr.predict(X)

    # Run crossvalidation predictions at the same time
    table['CrossPredict'] = cross_val_predict(lr, X, y, cv=X.shape[0])

    # How well did we do on crossvalidation?
    crossval_perf = explained_variance_score(y, table.CrossPredict)

    # How well did we do on direct?
    direct_perf = explained_variance_score(y, table.DirectPredict)

    return (direct_perf, crossval_perf, table, lr.coef_, lr.intercept_)


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

    # Do direct regression too
    lr.fit(X, y)
    data['DirectPredict'] = lr.predict(X)

    # Run crossvalidation predictions at the same time
    data['CrossPredict'] = cross_val_predict(lr, X, y, cv=X.shape[0])

    # How well did we do on crossvalidation?
    crossval_perf = explained_variance_score(y, data.CrossPredict)

    # How well did we do on direct?
    direct_perf = explained_variance_score(y, data.DirectPredict)

    return (direct_perf, crossval_perf, data)


def CALCapply(row):
    from .StoneModel import StoneMod
    from .StoneNRecep import StoneN
    from .StoneHelper import getMedianKx

    DCexpr = [2.0, 3.0, 2.0, 2.0]

    KaFull = [row.FcgRI + 0.00001, row.FcgRIIB, row.FcgRIII, row.FcgRIV]

    row['NK'] = StoneMod(logR=4.0, Ka=row.FcgRIII, v=row.v,
                         Kx=getMedianKx() * row.FcgRIII, L0=row.L0)[2]

    row['DC'] = StoneN(logR=DCexpr, Ka=KaFull, Kx=getMedianKx(),
                       gnu=row.v, L0=row.L0).getActivity([1, -1, 1, 1])

    row['2B-KO'] = 1

    if re.search('FcgRIIB-', row.name) is None:
        row['2B-KO'] = 0

    return row


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


def InVivoPredict(inn=[5, 1E-12]):
    """ Cross validate KnockdownLasso by using a pair of rows as test set """

    inn = np.squeeze(inn)

    # Collect data
    try:
        X, y, table = modelPrepAffinity(v=inn[0], L0=inn[1])
    except RuntimeError:
        return np.nan

    model = regFunc()
    model.fit(X, y)

    table['NKeff'] = table.NK * np.power(10, model.res.x[2])
    table['DCeff'] = table.DC * np.power(10, model.res.x[3])
    table['2Beff'] = table['2B-KO'] * np.power(10, model.res.x[4])

    pd.set_option('expand_frame_repr', False)

    table['CPredict'] = cross_val_predict(model, X, y, cv=len(y))
    table['DPredict'] = model.predict(X)
    table['NKfrac'] = table.NKeff / (table.DCeff + table.NKeff + table['2Beff'])
    table['Error'] = abs(table.CPredict - y)

    return (explained_variance_score(table.DPredict, y), explained_variance_score(table.CPredict, y), table, model)


def crossValF(table):
    yy = cross_val_predict(regFunc(),
                           table.drop('Effectiveness', axis=1),
                           table['Effectiveness'],
                           cv=table.shape[0])

    return explained_variance_score(yy, table['Effectiveness'])


def InVivoPredictMinusComponents():
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
        from scipy.optimize import least_squares

        # Fuction for fit residual
        diffF = lambda p: self.trainy - self.predict(p=p)

        self.trainX, self.trainy = X, y

        x0 = np.ones((X.shape[1] + 2, ), dtype=np.float64)
        lb = np.full(x0.shape, -20, dtype=np.float64)

        self.res = least_squares(diffF, x0=x0,
                                 jac='3-point', bounds=(lb, -lb))

        resC = least_squares(diffF, x0=x0 * 2,
                             jac='3-point', bounds=(lb, -lb))

        if resC.cost < self.res.cost:
            self.res = resC

    def predict(self, X=None, p=None):
        """
        Output prediction from parameter set. Use internal X if none given.
        """
        from scipy.stats import norm

        if p is None:
            p = self.res.x

        if self.logg is True:
            p = np.power(10, p)

        if X is None:
            X = self.trainX

        return norm.cdf(np.dot(X, p[2:]), loc=p[0], scale=p[1])
