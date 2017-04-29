import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def parallelize_dataframe(df, func):
    pool = Pool(cpu_count())

    iterpool = tqdm(pool.imap(func, np.vsplit(df, df.shape[0])), total=df.shape[0])

    df = np.fromiter(iterpool, dtype=np.float, count=df.shape[0])

    pool.close()
    pool.join()
    return df

correct = np.log10([0.0055, 0.358, 2.895, 0.0049])

def modelPrepAffinity(M, inn):
    from .StoneHelper import getMedianKx

    L0 = 1E-9
    v = 5
    data = M.NimmerjahnEffectTableAffinities()

    def NKapply(row):
        from .StoneModel import StoneMod

        return StoneMod(logR=4.0, Ka=row.FcgRIII, v=v, Kx=getMedianKx(), L0=L0, fullOutput = True)[2]

    def DCapply(row, Rin):
        from .StoneNRecep import StoneN

        aa = StoneN(logR=Rin, 
                    Ka=[row.FcgRI+0.00001, row.FcgRIIB, row.FcgRIII, row.FcgRIV], 
                    Kx=getMedianKx(),
                    gnu = v,
                    L0 = L0)

        rmulti = aa.getRmultiAll()

        return np.sum(rmulti) - 2*rmulti[1]

    data['NK'] = data.apply(NKapply, axis=1)
    data['DC'] = data.apply(lambda x: DCapply(x, [1.0, 2.0, 1.0, 1.0] + correct + inn), axis=1)
    data['neut'] = data.apply(lambda x: DCapply(x, [1.0, 2.0, 4.0, 4.0] + correct + inn), axis=1)

    data.loc['None', :] = 0.0

    data = data.iloc[:, 4:]

    # Assign independent variables and dependent variable
    X = data.drop('Effectiveness', axis=1)

    y = data['Effectiveness'].as_matrix()

    return (X.as_matrix(), y, data)


def varyExpr():
    lvls = np.arange(-1.0, 3.0, 0.5, dtype=np.float)

    pp = pd.DataFrame(np.array(np.meshgrid(lvls, lvls, lvls, lvls)).T.reshape(-1,4))
    pp.columns = ['R1', 'R2', 'R3', 'R4']

    pp['Fit'] = parallelize_dataframe(pp.as_matrix(), InVivoPredict)

    ppp.to_csv('outtt.csv')


def InVivoPredict(inn=[0, 0, 0, 0]):
    """ Cross validate KnockdownLasso by using a pair of rows as test set """
    from sklearn.model_selection import cross_val_predict
    from sklearn.metrics import explained_variance_score
    from .StoneModMouse import StoneModelMouse

    inn = np.squeeze(inn)

    # Collect data
    X, y, table = modelPrepAffinity(StoneModelMouse(), inn)
    model = regFunc()

    model.fit(X, y)

    #pd.set_option('expand_frame_repr', False)
    
    #xx = cross_val_predict(model, X, y, cv=len(y))

    table['Error'] = abs(model.predict(X) - y)
    #table['CPredict'] = xx
    table['DPredict'] = model.predict(X)

    #print('')

    #print(table)

    #print(explained_variance_score(model.predict(X), y))

    return explained_variance_score(model.predict(X), y)



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

        x0 = np.zeros((X.shape[1] + 2, ), dtype=np.float)

        self.res = least_squares(lambda p: self.diffF(p), 
                            x0=x0, 
                            jac='3-point')

    def predict(self, X):
        return self.outF(self.res.x, X)
