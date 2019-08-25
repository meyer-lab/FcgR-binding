import numpy as np
from sklearn.base import BaseEstimator
from sklearn.preprocessing import StandardScaler
from scipy.optimize import least_squares, lsq_linear
from scipy.special import expm1


class regFunc(BaseEstimator):
    """ Class to handle regression with saturating effect. """

    def __init__(self):
        self.res, self.trainX, self.trainy = None, None, None
        self.scale = StandardScaler(copy=True, with_mean=False, with_std=True)

    def fit(self, X, y):
        """ Fit the X-y relationship. Return nothing. """
        self.trainX, self.trainy = self.scale.fit_transform(np.array(X)), np.array(y)

        bnds = (0.0, np.inf)

        # Use OLS estimate as starting point
        x0 = lsq_linear(self.trainX, self.trainy, bounds=bnds).x

        # Run least_squares step
        self.res = least_squares(self.residual, x0=x0, bounds=bnds,
                                 jac=self.jac, ftol=None, gtol=None)

    def residual(self, p):
        """ Helper function that returns fitting residual. """
        return self.predict(p=p) - self.trainy

    def jac(self, p):
        """ Jacobian of exponential prediction function. """
        return np.exp(-np.dot(self.trainX, p))[:, np.newaxis] * self.trainX

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

        return -expm1(-np.dot(X, p))
