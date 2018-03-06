import numpy as np
from sklearn.base import BaseEstimator
from scipy.optimize import least_squares, differential_evolution
from numba import jit


@jit(nopython=True)
def jac(p, X, logg):
    """ Jacobian for fitting. """
    if logg is True:
        p = np.power(10, p)

    # Find inner term.
    yy = np.reciprocal(np.square(np.cosh(np.dot(X, p))))

    return np.outer(yy, p)


@jit(nopython=True)
def predict(p, X, logg):
    """ Core prediction function. """
    if logg is True:
            p = np.power(10, p)

    return np.tanh(np.dot(X, p))


@jit(nopython=True)
def diffEvo(p, X, logg, y):
    return np.sum(np.square(predict(p, X, logg) - y))


class regFunc(BaseEstimator):
    """ Class to handle regression with saturating effect. """

    def __init__(self, logg=True):
        self.logg = logg
        self.res, self.trainX, self.trainy = None, None, None

    def fit(self, X, y):
        """ Fit the X-y relationship. Return nothing. """
        self.trainX, self.trainy = np.array(X), np.array(y)

        ub = np.full((X.shape[1], ), 12.0)

        res = differential_evolution(diffEvo, bounds=list(zip(-ub, ub)), disp=False, args=(self.trainX, self.logg, self.trainy))

        self.res = least_squares(self.diffF, x0=res.x, jac=jac, bounds=(-ub, ub), args=(self.trainX, self.logg))

    def diffF(self, p, X, logg):
        return self.trainy - predict(p, X, logg)

    def predict(self, X=None, p=None):
        """
        Output prediction from parameter set. Use internal X if none given.
        """

        if p is None:
            p = self.res.x

        if X is None:
            X = self.trainX

        return predict(p, np.array(X), self.logg)
