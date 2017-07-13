import numpy as np
from sklearn.base import BaseEstimator


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
