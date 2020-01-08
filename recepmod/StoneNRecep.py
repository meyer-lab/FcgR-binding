import numpy as np
from scipy.optimize import root


def Req_func(Req, Rtot, L0fA, AKxStar, f):
    """ Mass balance. Transformation to account for bounds. """
    Phisum = np.dot(AKxStar, Req.T)
    return Req + L0fA * Req * (1 + Phisum)**(f - 1) - Rtot


def polyfc(L0, KxStar, f, Rtot, IgGC, Kav, ActV=None):
    """
    The main function. Generate all info for heterogenenous binding case
    L0: concentration of ligand.
    KxStar: detailed balance-corrected Kx.
    f: valency
    Rtot: numbers of each receptor appearing on the cell.
    IgGC: the composition of the mixture IgGC used.
    Kav: a matrix of Ka values. row = IgG's, col = FcgR's
    (Optional: the activity indices ActV)
    """
    # Data consistency check
    Kav = np.array(Kav)
    Rtot = np.array(Rtot)
    assert Rtot.ndim <= 1
    IgGC = np.array(IgGC)
    assert IgGC.ndim <= 1
    IgGC = IgGC / np.sum(IgGC)
    assert IgGC.size == Kav.shape[0]
    assert Rtot.size == Kav.shape[1]
    assert Kav.ndim == 2

    # Run least squares to get Req
    Req = Req_Regression(L0, KxStar, f, Rtot, IgGC, Kav)

    nr = Rtot.size  # the number of different receptors
    ni = IgGC.size  # the number of different IgG's

    Phi = np.ones((ni, nr + 1)) * IgGC.reshape(-1, 1)
    Phi[:, :nr] *= Kav * Req * KxStar
    Phisum = np.sum(Phi[:, :nr])
    Phisum_n = np.sum(Phi[:, :nr], axis=0)

    w = dict()
    w['Lbound'] = L0 / KxStar * ((1 + Phisum)**f - 1)
    w['Rbound'] = L0 / KxStar * f * Phisum * (1 + Phisum)**(f - 1)
    w['Rbound_n'] = L0 / KxStar * f * Phisum_n * (1 + Phisum)**(f - 1)
    w['Rmulti'] = L0 / KxStar * f * Phisum * ((1 + Phisum)**(f - 1) - 1)
    w['Rmulti_n'] = L0 / KxStar * f * Phisum_n * ((1 + Phisum)**(f - 1) - 1)
    w['nXlink'] = L0 / KxStar * (1 + (1 + Phisum)**(f - 1) * ((f - 1) * Phisum - 1))
    w['Req'] = Req

    if isinstance(f, int):  # Allow float valencies, but then skip vieq
        w['vieq'] = L0 / KxStar * sp.special.comb(f, range(f + 1)) * Phisum**range(f + 1)

    w['vtot'] = L0 / KxStar * (1 + Phisum)**f
    if ActV is not None:
        ActV = np.array(ActV).reshape(1, -1)
        assert ActV.size == nr
        w['ActV'] = max(np.dot(w['Rmulti_n'], ActV.T)[0], 0)
    return w


def Req_Regression(L0, KxStar, f, Rtot, IgGC, Kav):
    '''Run least squares regression to calculate the Req vector'''
    A = np.dot(IgGC.T, Kav)
    L0fA = L0 * f * A
    AKxStar = A * KxStar

    # Identify an initial guess just on max monovalent interaction
    # Correction factor at end is just empirical
    x0 = np.max(L0fA, axis=0)
    x0 = np.multiply(1.0 - np.divide(x0, 1 + x0), Rtot)

    # Solve Req by calling least_squares() and Req_func()
    lsq = root(Req_func, x0, method="lm", args=(Rtot, L0fA, AKxStar, f), options={'maxiter': 3000})

    assert lsq['success'], \
        "Failure in rootfinding. " + str(lsq)

    return lsq['x'].reshape(1, -1)





class StoneN:
    """ Use a class to keep track of the various parameters. """

    def getRbnd(self):
        """ Return the amount of each receptor that is bound. """
        return self.w["Rbound"]

    def getLbnd(self):
        """ Return the amount of ligand bound. """
        return self.w["Lbound"]

    def getRmultiAll(self):
        """ Return the amount of each receptor that is found in more than a monovalent complex. """
        return self.w["Rmulti_n"]

    def getActivity(self, actV):
        """ Return the activity index. """
        return np.maximum(0.0, np.dot(self.getRmultiAll(), actV))

    def __init__(self, logR, Ka, Kx, gnu, L0):
        self.logR = np.array(logR, dtype=np.float, copy=True)
        self.Ka = np.array(Ka, dtype=np.float, copy=True)
        self.Kx = np.array(Kx * Ka[0], dtype=np.float, copy=True)
        self.gnu = np.array(gnu, dtype=np.int, copy=True)
        self.L0 = np.array(L0, dtype=np.float, copy=True)

        if len(self.logR) != len(self.Ka):
            raise IndexError("logR and Ka must be same length.")
        elif np.any(np.isnan(self.logR)):
            raise ValueError("logR has nan value.")
        elif np.any(np.isnan(self.Ka)):
            raise ValueError("Ka has nan value.")

        self.w = polyfc(self.L0, self.Kx / Ka[0], self.gnu, np.power(10, self.logR), np.array([1.0]), self.Ka.reshape(1, -1))
