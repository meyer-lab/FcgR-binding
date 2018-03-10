import numpy as np
from sklearn.base import BaseEstimator
from scipy.optimize import least_squares, basinhopping
from sklearn.preprocessing import StandardScaler
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


@jit(f8(f8[:], f8[:,:], b1, f8[:]), cache=True)
def diffEvoJac(p, X, logg, y):
    r = predict(p, X, logg) - y
    J = jac(p, X, logg, y)

    return np.dot(np.transpose(J), r)


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

        ub = np.full((X.shape[1], ), 12.0)

        args = (self.trainX, self.logg, self.trainy)

        minimizer_kwargs = {"method": "BFGS", "jac":diffEvoJac, "args":args}

        res = basinhopping(diffEvo, x0=ub-ub, minimizer_kwargs=minimizer_kwargs)

        self.res = least_squares(residDiff, x0=np.minimum(np.maximum(res.x, -ub), ub), jac=jac,
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
        else:
            X = self.scale.transform(np.array(X))

        return predict(p, X, self.logg)
