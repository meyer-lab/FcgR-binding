import numpy as np
from sklearn.base import BaseEstimator
from sklearn.preprocessing import StandardScaler
from scipy.optimize import least_squares
from scipy.special import expm1


def predict(p, X, logg):
    """ Core prediction function. """
    if logg is True:
        p = np.power(10, p)

    return -expm1(-np.dot(X, p))


def residDiff(p, X, logg, y):
    return predict(p, X, logg) - y


class regFunc(BaseEstimator):
    """ Class to handle regression with saturating effect. """

    def __init__(self, logg=True):
        self.logg = logg
        self.res, self.trainX, self.trainy = None, None, None
        self.scale = StandardScaler(copy=True, with_mean=False, with_std=True)

    def fit(self, X, y):
        """ Fit the X-y relationship. Return nothing. """
        self.trainX, self.trainy = self.scale.fit_transform(np.array(X)), np.array(y)

        # Package up data
        args = (self.trainX, self.logg, self.trainy)

        if self.logg:
            bnds = (-np.inf, 20)
        else:
            bnds = (0.0, np.inf)

        # Run least_squares step
        self.res = least_squares(residDiff, x0=np.zeros(X.shape[1]), args=args, bounds=bnds)

    def predict(self, X=None, p=None):
        """
        Output prediction from parameter set. Use internal X if none given.
        """

        if p is None:
            p = self.res.x

        if X is None:
            X = self.trainX
        else:
            X = self.scale.transform(np.array(X))

        return predict(p, X, self.logg)
