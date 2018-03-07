import numpy as np
from sklearn.base import BaseEstimator
from scipy.optimize import least_squares, differential_evolution
from numba import jit, f8, b1


@jit(f8[:,:](f8[:], f8[:,:], b1, f8[:]), nopython=True, cache=True, nogil=True)
def jac(p, X, logg, _):
    """ Jacobian for fitting. """
    if logg is True:
        p = np.power(10, p)

    # Find inner term.
    yy = np.reciprocal(np.square(np.cosh(np.dot(X, p))))

    return np.outer(yy, p)


@jit(f8[:](f8[:], f8[:,:], b1), nopython=True, cache=True, nogil=True)
def predict(p, X, logg):
    """ Core prediction function. """
    if logg is True:
        p = np.power(10, p)

    return np.tanh(np.dot(X, p))


@jit(f8(f8[:], f8[:,:], b1, f8[:]), nopython=True, cache=True, nogil=True)
def diffEvo(p, X, logg, y):
    return np.sum(np.square(predict(p, X, logg) - y))


@jit(f8[:](f8[:], f8[:,:], b1, f8[:]), nopython=True, cache=True, nogil=True)
def residDiff(p, X, logg, y):
    return predict(p, X, logg) - y


class regFunc(BaseEstimator):
    """ Class to handle regression with saturating effect. """

    def __init__(self, logg=True):
        self.logg = logg
        self.res, self.trainX, self.trainy = None, None, None

    def fit(self, X, y):
        """ Fit the X-y relationship. Return nothing. """
        self.trainX, self.trainy = np.array(X), np.array(y)

        ub = np.full((X.shape[1], ), 12.0)

        args = (self.trainX, self.logg, self.trainy)

        res = differential_evolution(diffEvo,
                                     popsize=30,
                                     bounds=list(zip(-ub, ub)),
                                     disp=False,
                                     args=args)

        self.res = least_squares(residDiff, x0=res.x, jac=jac,
                                 tr_solver='exact', method='dogbox',
                                 bounds=(-ub, ub), args=args)

    def predict(self, X=None, p=None):
        """
        Output prediction from parameter set. Use internal X if none given.
        """

        if p is None:
            p = self.res.x

        if X is None:
            X = self.trainX

        return predict(p, np.array(X), self.logg)
