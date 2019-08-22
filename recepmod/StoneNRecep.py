import numpy as np
from fcBindingModel import polyfc


class StoneN():
    """ Use a class to keep track of the various parameters. """

    def getRbnd(self):
        """ Return the amount of each receptor that is bound. """
        return self.w["Rbound"]

    def getLbnd(self):
        """ Return the amount of ligand bound. """
        return self.w["Lbound"]

    def getRmultiAll(self):
        """ Return the amount of each receptor that is found in more than a monovalent complex. """
        return self.w["Rmulti"]

    def getActivity(self, actV):
        """ Return the activity index. """
        actV = np.array(actV)
        return max(np.dot(self.w['Rmulti_n'], actV.T), 0)

    def __init__(self, logR, Ka, Kx, gnu, L0):
        self.logR = np.array(logR, dtype=np.float, copy=True)
        self.Ka = np.array(Ka, dtype=np.float, copy=True)
        self.Kx = np.array(Kx * Ka[0], dtype=np.float, copy=True)
        self.gnu = np.array(gnu, dtype=np.int, copy=True)
        self.L0 = np.array(L0, dtype=np.float, copy=True)

        assert len(self.logR) == len(self.Ka), "logR and Ka must be same length."
        assert np.all(np.finite(self.logR)), "logR has nan value."
        assert np.all(np.finite(self.Ka)), "Ka has nan value."

        self.w = polyfc(self.L0, self.Kx, self.gnu, 10 ** self.logR, np.array([1.0]), self.Ka.reshape((1, -1)))
