import numpy as np
from sklearn.base import BaseEstimator
from scipy.optimize import least_squares, differential_evolution


class regFunc(BaseEstimator):
    """ Class to handle regression with saturating effect. """

    def __init__(self, logg=True):
        self.logg = logg
        self.res, self.trainX, self.trainy = None, None, None

    def fit(self, X, y):
        """ Fit the X-y relationship. Return nothing. """
        self.trainX, self.trainy = X, y

        ub = np.full((X.shape[1], ), 12.0)

        #res = differential_evolution(lambda p: np.sum(np.square(self.trainy - self.predict(p=p))),
        #                             bounds=list(zip(-ub, ub)), disp=False)

        self.res = least_squares(self.diffF, x0=ub - ub, jac='cs', bounds=(-ub, ub)) # res.x

    def diffF(self, p):
        return self.trainy - self.predict(p=p)

    def predict(self, X=None, p=None):
        """
        Output prediction from parameter set. Use internal X if none given.
        """

        if p is None:
            p = self.res.x

        if self.logg is True:
            p = np.power(10, p)

        if X is None:
            X = self.trainX

        return np.tanh(np.dot(X, p))
