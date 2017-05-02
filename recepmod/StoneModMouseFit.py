import re
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import explained_variance_score
from .StoneModMouse import StoneModelMouse
from .StoneHelper import parallelize_dataframe

def NimmerjahnPredictByAffinities():
    """ This will run ordinary linear regression using just affinities of receptors. """

    # Run regression with our setup
    lr = regFunc()

    data = StoneModelMouse().NimmerjahnEffectTableAffinities()
    data['ActMax'] = data.apply(lambda x: max(x.FcgRI, x.FcgRIII, x.FcgRIV), axis=1)

    X = data[['ActMax', 'FcgRIIB']]
    y = data['Effectiveness']

    # Log transform to keep ratios
    X = X.apply(np.log2).replace(-np.inf, -3)

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

def modelPrepAffinity(M, v=5, L0=1E-12):
    from .StoneHelper import getMedianKx

    data = M.NimmerjahnEffectTableAffinities()

    DCexpr = [3.0, 4.0, 3.0, 3.0]

    def CALCapply(row):
        from .StoneModel import StoneMod
        from .StoneNRecep import StoneN

        KaFull = [row.FcgRI+0.00001, row.FcgRIIB, row.FcgRIII, row.FcgRIV]

        row['NK'] = StoneMod(logR=4.0, Ka=row.FcgRIII, v=v, Kx=getMedianKx(), L0=L0, fullOutput = True)[2]
        row['DC'] = StoneN(logR=DCexpr, Ka=KaFull, Kx=getMedianKx(), gnu=v, L0=L0).getActivity([1, -1, 1, 1])

        if re.search('FcgRIIB-', row.name) is None:
            row['2B-KO'] = 0
        else:
            row['2B-KO'] = 1

        return row

    data = data.apply(CALCapply, axis=1)

    data.loc['None', :] = 0.0

    data = data.iloc[:, 4:]

    # Assign independent variables and dependent variable
    X = data.drop('Effectiveness', axis=1)

    y = data['Effectiveness'].as_matrix()

    return (X.as_matrix(), y, data)


def varyExpr():
    gnus = np.arange(2, 10, 1, dtype=np.float)
    Los = np.power(10, np.arange(-12, -6, 0.5, dtype=np.float))

    pp = pd.DataFrame(np.array(np.meshgrid(gnus, Los)).T.reshape(-1,2))
    pp.columns = ['gnus', 'Los']

    pp['Fit'] = parallelize_dataframe(pp.as_matrix(), InVivoPredict)

    pp.to_csv('outtt.csv')


def InVivoPredict(inn=[5, 1E-12], printt=False):
    """ Cross validate KnockdownLasso by using a pair of rows as test set """

    inn = np.squeeze(inn)

    # Collect data
    try:
        X, y, table = modelPrepAffinity(StoneModelMouse(), v=inn[0], L0=inn[1])
    except RuntimeError:
        return np.nan

    model = regFunc()
    model.fit(X, y)

    pd.set_option('expand_frame_repr', False)
    
    table['CPredict'] = cross_val_predict(model, X, y, cv=len(y))
    table['DPredict'] = model.predict(X)
    table['NKeff'] = table.NK * model.res.x[2]
    table['DCeff'] = table.DC * model.res.x[3]
    table['NKfrac'] = table.NKeff / (table.DCeff + table.NKeff)
    table['Error'] = abs(table.CPredict - y)

    if printt is True:
        print('')
        print(table)

    return (explained_variance_score(table.DPredict, y), explained_variance_score(table.CPredict, y), table)


class regFunc(BaseEstimator):
    def outF(self, p, X=None):
        from scipy.stats import norm

        p = np.power(10, p)

        if X is None:
            X = self.trainX

        return norm.cdf(np.dot(X, p[2:]), loc=p[0], scale=p[1])

    def diffF(self, p):
        return self.trainy - self.outF(p)

    def errF(self, p):
        from numpy.linalg import norm

        return norm(self.diffF(p))

    def fit(self, X, y):
        from scipy.optimize import least_squares

        self.trainX, self.trainy = X, y

        x0 = np.zeros((X.shape[1] + 2, ), dtype=np.float64)
        lb = np.full(x0.shape, -20, dtype=np.float64)
        ub = np.full(x0.shape, 20, dtype=np.float64)

        self.res = least_squares(lambda p: self.diffF(p), 
                            x0=x0, 
                            jac='3-point',
                            bounds=(lb, ub))

    def predict(self, X):
        return self.outF(self.res.x, X)
