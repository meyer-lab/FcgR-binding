import re
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from .StoneTwoRecep import StoneTwo
from .StoneNRecep import StoneN
from .StoneHelper import getMedianKx

def modelPrepAffinity(M):
    L0 = 1E-8
    v = 2
    data = M.NimmerjahnEffectTableAffinities()

    def NKapply(row):
        aa = StoneTwo(logR=[4.0, -6.0], Ka=[row.FcgRIII, 1.0], Kx=getMedianKx())

        outt = aa.getAllProps(v, L0)

        return outt.activity

    def DCapply(row):
        aa = StoneN(logR=[1.0, 4.0, 3.0, 3.0], 
                    Ka=[row.FcgRI+1, row.FcgRIIB, row.FcgRIII, row.FcgRIV], 
                    Kx=getMedianKx(),
                    gnu = v,
                    L0 = L0)

        return aa.getActBnd()

    data['NK'] = data.apply(NKapply, axis=1)
    data['DC'] = data.apply(DCapply, axis=1)

    data = data.iloc[:, 4:]

    # Assign independent variables and dependent variable
    X = data.drop('Effectiveness', axis=1)

    y = data['Effectiveness'].as_matrix()

    return (X.as_matrix(), y, data)


def InVivoPredict(M):
    """ Cross validate KnockdownLasso by using a pair of rows as test set """
    from sklearn.model_selection import cross_val_predict
    from sklearn.metrics import explained_variance_score

    # Collect data
    X, y, table = modelPrepAffinity(M)
    model = regFunc()

    

    table.to_csv('out.csv')


    model.fit(X, y)
    print(explained_variance_score(model.predict(X), y))

    pd.set_option('expand_frame_repr', False)
    
    xx = cross_val_predict(model, X, y, cv=len(y))

    print(explained_variance_score(xx, y))

    table['Error'] = abs(xx - y)
    table['CPredict'] = xx

    print(table)

    return None



class regFunc(BaseEstimator):
    def outF(self, X, p):
        from scipy.special import expit

        return expit(np.dot(X, p[1:]) - p[0])

    def fit(self, X, y):
        from scipy.optimize import least_squares

        x0 = np.zeros((X.shape[1]+1,), dtype=np.float64)

        lb = np.full(x0.shape, -10)
        ub = np.full(x0.shape, 10)

        self.res = least_squares(lambda p: y - self.outF(X, p), x0, bounds=(lb, ub))

    def predict(self, X):
        return self.outF(X, self.res.x)