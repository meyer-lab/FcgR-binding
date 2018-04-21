import numpy as np
from sklearn.base import BaseEstimator
from sklearn.preprocessing import StandardScaler
from scipy.optimize import least_squares, basinhopping
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
    return np.sum(np.square(predict(p, X, logg) - y))/2.0


@jit(f8[:](f8[:], f8[:,:], b1, f8[:]), nopython=True, cache=True, nogil=True)
def diffEvoJac(p, X, logg, y):
    return np.dot(jac(p, X, logg, y).transpose(), predict(p, X, logg) - y)


@jit(f8[:](f8[:], f8[:,:], b1, f8[:]), nopython=True, cache=True, nogil=True)
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

        if X.shape[1] == 5:
            x0 = np.array([-0.4, -6.0, -0.4, -6.0, -0.4])
        else:
            x0 = np.zeros(X.shape[1])

        # Run initial global search
        res = basinhopping(diffEvo, niter=2000, x0=x0, stepsize=0.1,
                           minimizer_kwargs={"jac":diffEvoJac, "args":args})

        # Run least_squares step
        self.res = least_squares(residDiff, x0=res.x, jac=jac,
                                 tr_solver='exact', method='lm', args=args)

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
