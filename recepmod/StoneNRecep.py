import numpy as np
from memoize import memoize
from .StoneModel import nchoosek


def StoneVgrid(Req, Ka, gnu, Kx, L0):
    """
    This function takes in the relevant parameters and creates the v_ij grid
    Kx should be the Kx of Ka[0]
    Ka should be a tuple of size N with each affinity
    Req should be a tuple of size N
    """

    # Get vGrid with the combinatorics all worked out
    vGrid = vGridInit(gnu, len(Req)) * (L0 * Ka[0] / Kx)

    # Precalculate outside terms
    KKRK = np.multiply(Ka, Req) / Ka[0] * Kx

    for ii in range(vGrid.ndim):
        # Setup the slicing for the matrix portion we want
        slicing = list((slice(None), ) * ii + (1, ) + (slice(None), ) * (vGrid.ndim - ii - 1))

        term = KKRK[ii]

        vGrid[slicing] *= term

        for jj in range(2, gnu + 1):
            slicing[ii] = jj

            term *= KKRK[ii]

            vGrid[slicing] *= term

    return vGrid


def boundMult(cur_pos):
    """ Deal with the combinatorics of different species bound. """
    upos = np.array(cur_pos, dtype=np.int)
    upos = np.sort(upos[upos > 0])

    if len(upos) == 1:
        return 1

    outt = 1

    while len(upos) > 1:
        outt *= nchoosek(sum(upos))[upos[0]]
        upos = np.delete(upos, 0)

    return outt


@memoize
def vGridInit(gnu, Nrep):
    """ Make the grid of all the possible multimerization states. """

    # Initialize the grid of possibilities
    vGrid = np.zeros(np.full((Nrep, ), gnu + 1), dtype=np.float)

    # Precalculate outside terms
    nk = nchoosek(gnu)

    for cur_pos in np.ndindex(vGrid.shape):
        scur = sum(cur_pos)

        if scur <= gnu and scur > 0:
            vGrid[cur_pos] = nk[scur] * boundMult(cur_pos)

    return vGrid


def sumNonDims(vGridIn, dimm):
    """ Collapse array along nonfocus dimensions. """
    if dimm > len(vGridIn.shape):
        raise IndexError("sumNonDims: Dimension to keep is out of range.")

    vGridIn = vGridIn.copy()

    for ii in reversed(range(len(vGridIn.shape))):
        if ii != dimm:
            vGridIn = np.sum(vGridIn, axis=ii)

    return vGridIn


def StoneRbnd(vGrid):
    """ This calculates the Rbnd quantity from a v_ij... grid """

    # Vector to multiply by for Rbnd
    RbndV = np.arange(vGrid.shape[0])

    # Multiply by number of receptors in each case
    genF = np.vectorize(lambda xx: np.sum(np.multiply(sumNonDims(vGrid, xx), RbndV)))

    vv = np.arange(len(vGrid.shape), dtype=np.int)

    return genF(vv)


def StoneRmultiAll(vGrid):
    """ This is the number of receptors multimerized with self or non-self """
    from itertools import permutations

    vGrid = np.copy(vGrid)
    idx = np.zeros((len(vGrid.shape), ), dtype=np.intp)
    idx[0] = 1

    # Erase species that are bound all on their own
    for perm in permutations(idx):
        vGrid[perm] = 0.0

    # Just Rbnd from here
    return StoneRbnd(vGrid)


def reqSolver(logR, Ka, gnu, Kx, L0):
    """ Solve for Req """
    from scipy.optimize import brentq, root

    R = np.power(10.0, logR)

    # This is the error function to find the root of
    def rootF(curr, ii=None, x=None):
        """ Mass balance calculator we want to solve. """
        # If we're overriding one axis do it here.
        if ii is not None:
            curr = curr.copy()
            curr[ii] = x

        # Convert out of logs, minimum prevents overflow errors when no bounds
        curr = np.power(10, np.minimum(curr, logR))

        # Collect the Rbnd quantities
        Rbnd = StoneRbnd(StoneVgrid(curr, Ka, gnu, Kx, L0))

        # Req is the unbound receptor, so perform a mass balance
        return R - curr - Rbnd

    # Reasonable approximation for curReq
    curReq = np.array(logR - Ka * L0, dtype=np.float64)

    if np.max(np.multiply(rootF(np.full(logR.shape, -200, dtype=np.float)), rootF(logR))) > 0:
        raise RuntimeError("No reasonable value for Req exists.")

    sol = root(fun=rootF, x0=curReq, method='hybr')

    if sol.success is True:
        return np.minimum(sol.x, logR)

    # Set jj so linting doesn't complain
    jj = 0

    # Receptors only weakly interact, so try and find the roots separately in an iterive fashion
    for _ in range(200):
        # Square the error for each
        error = np.square(rootF(curReq))

        # If the norm error is sufficiently reduced leave
        if np.sum(error) < 1.0E-12:
            return np.minimum(curReq, logR)

        # Find receptor to optimize
        jj = np.argmax(error)

        # Dig up the index to optimize. Focus on the worst receptor.
        curReq[jj] = brentq(lambda x: rootF(curReq, jj, x)[jj], -200, logR[jj], disp=False)

    raise RuntimeError("The reqSolver couldn't find Req in a reasonable number of iterations.")


class StoneN:
    """ Use a class to keep track of the various parameters. """

    def getRbnd(self):
        """ Return the amount of each receptor that is bound. """
        return StoneRbnd(self.vgridOut)

    def getLbnd(self):
        """ Return the amount of ligand bound. """
        return np.sum(self.vgridOut)

    def getRmultiAll(self):
        """ Return the amount of each receptor that is found in more than a monovalent complex. """
        return StoneRmultiAll(self.vgridOut)

    def getActivity(self, actV):
        """ Return the activity index. """
        summ = np.dot(self.getRmultiAll(), actV)

        if summ >= 0:
            return summ
        elif summ < 0:
            return 0.0

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

        self.Req = reqSolver(self.logR, self.Ka, self.gnu, self.Kx, self.L0)

        self.vgridOut = StoneVgrid(np.power(10, self.Req), self.Ka, self.gnu, self.Kx, self.L0)
