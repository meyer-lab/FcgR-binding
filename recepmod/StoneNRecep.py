import numpy as np
from memoize import memoize
from fcBindingModel import Req_Regression
from .StoneModel import nchoosek


def StoneVgrid(Req, Ka, gnu, Kx, L0):
    """
    This function takes in the relevant parameters and creates the v_ij grid
    Kx should be the Kx of Ka[0]
    Ka should be a tuple of size N with each affinity
    Req should be a tuple of size N
    """

    # Get vGrid with the combinatorics all worked out
    vGrid = vGridInit(gnu, Req.size) * (L0 * Ka[0] / Kx)

    # Precalculate outside terms
    KKRK = np.multiply(Ka, Req) / Ka[0] * Kx

    for ii in range(vGrid.ndim):
        # Setup the slicing for the matrix portion we want
        slicing = list((slice(None), ) * ii + (1, ) + (slice(None), ) * (vGrid.ndim - ii - 1))

        term = KKRK[ii]

        vGrid[tuple(slicing)] *= term

        for jj in range(2, gnu + 1):
            slicing[ii] = jj

            term *= KKRK[ii]

            vGrid[tuple(slicing)] *= term

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
    assert dimm < vGridIn.ndim, "sumNonDims: Dimension to keep is out of range."

    dimss = tuple([i for i in range(vGridIn.ndim) if i != dimm])

    return np.sum(vGridIn, axis=dimss)


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

        if summ < 0:
            return 0.0
        return summ

    def __init__(self, logR, Ka, Kx, gnu, L0):
        self.logR = np.array(logR, dtype=np.float, copy=True)
        self.Ka = np.array(Ka, dtype=np.float, copy=True)
        self.Kx = np.array(Kx * Ka[0], dtype=np.float, copy=True)
        self.gnu = int(gnu)
        self.L0 = np.array(L0, dtype=np.float, copy=True)

        if len(self.logR) != len(self.Ka):
            raise IndexError("logR and Ka must be same length.")
        elif np.any(np.isnan(self.logR)):
            raise ValueError("logR has nan value.")
        elif np.any(np.isnan(self.Ka)):
            raise ValueError("Ka has nan value.")

        self.Req = Req_Regression(self.L0.copy(), self.Kx.copy(), self.gnu, np.power(10, self.logR), np.array([1.0]), self.Ka.reshape(1, -1))
        self.Req = np.squeeze(self.Req)
        
        assert self.Req.size == self.Ka.size

        self.vgridOut = StoneVgrid(self.Req, self.Ka, self.gnu, self.Kx, self.L0)
