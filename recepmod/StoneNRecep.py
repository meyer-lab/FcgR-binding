import numpy as np
import pandas as pd
from memoize import memoize
from .StoneModel import nchoosek


def StoneVgrid(Req, Ka, gnu, Kx, L0):
    """
    This function takes in the relevant parameters and creates the v_ij grid
    Kx should be the Kx of Ka[0]
    Ka should be a tuple of size N with each affinity
    Req should be a tuple of size N
    """

    if len(Req) != len(Ka):
        raise IndexError("Req and Ka must be same length.")

    # Get vGrid with the combinatorics all worked out
    vGrid = vGridInit(gnu, len(Req))

    # Precalculate outside terms
    vGrid = vGrid * L0 * Ka[0] / Kx
    KKRK = np.multiply(Ka, Req) / Ka[0] * Kx

    for cur_pos in np.ndindex(vGrid.shape):
        if vGrid[cur_pos] > 0:
            vGrid[cur_pos] *= np.power(KKRK, cur_pos).prod()

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

    # Initialize the grid of possibilities
    vGrid = np.zeros(np.full((Nrep, ), gnu+1), dtype=np.float)

    # Precalculate outside terms
    nk = nchoosek(gnu)

    for cur_pos in np.ndindex(vGrid.shape):
        scur = sum(cur_pos)

        if scur <= gnu and scur > 0:
            vGrid[cur_pos] = nk[scur] * boundMult(cur_pos)

    return(vGrid)


def sumNonDims(vGridIn, dimm):
    """ Collapse array along nonfocus dimensions. """
    if dimm > len(vGridIn.shape):
        raise IndexError("sumNonDims: Dimension to keep is out of range.")

    vGridIn = vGridIn.copy()

    for ii in range(len(vGridIn.shape)):
        if ii != dimm:
            vGridIn = np.sum(vGridIn, axis=ii, keepdims=True)

    vGridIn = np.squeeze(vGridIn)

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


def reqSolver(logR,Ka,gnu,Kx,L0):
    """ Solve for Req """
    from scipy.optimize import brentq
    from numpy.linalg import norm

    R = np.power(10.0, logR)

    # This is the error function to find the root of
    def rootF(x):
        # Convert out of logs
        x = np.power(10, x)

        # Collect the v_ij grid
        gridd = StoneVgrid(x,Ka,gnu,Kx,L0)

        # Collect the Rbnd quantities
        Rbnd = StoneRbnd(gridd)

        # Req is the unbound receptor, so perform a mass balance
        return R - x - Rbnd

    def overF(curr, ii, x):
        curr = curr.copy()
        curr[ii] = x

        return rootF(curr)[ii]

    curReq = np.full(logR.shape, -60, dtype = np.float)
    prevReq = curReq.copy()

    if np.max(np.multiply(rootF(curReq), rootF(logR))) > 0:
        return np.full(logR.shape, np.nan, dtype=np.float)

    # The two receptors only weakly interact, so try and find the roots separately in an iterive fashion
    for ii in range(200):
        if norm(rootF(curReq)) < 1.0E-7 and norm(curReq - prevReq) < 1E-7:
            return curReq
        else:
            prevReq = curReq

        # Dig up the index to optimize
        jj = ii % len(curReq)

        curReq[jj] = brentq(lambda x: overF(curReq, jj, x), -60, logR[jj], disp=False)

    return np.full(logR.shape, np.nan, dtype=np.float)


class StoneN:
    def getRbnd(self):
        return StoneRbnd(self.vgridOut)

    def getRmultiAll(self):
        return StoneRmultiAll(self.vgridOut)

    def getActivity(self, actV):
        vGrid = np.copy(self.vgridOut)
        actV = np.array(actV, dtype=np.float)

        # ii, jj is the number of receptor one, two bound
        it = np.nditer(vGrid, flags=['multi_index'], op_flags=['readwrite'])

        while not it.finished:
            if np.dot(it.multi_index, actV) < 0:
                it[0] = 0.0
            elif np.sum(it.multi_index) < 2:
                it[0] = 0.0
            else:
                it[0] *= np.dot(it.multi_index, actV)

            it.iternext()

        return np.sum(vGrid)

    def getAllProps(self):
        return pd.Series(dict(ligand=self.L0,
                              avidity=self.gnu,
                              ligandEff=self.L0*self.gnu,
                              Kx=self.Kx,
                              Rbnd=self.getRbnd()))


    def __init__(self, logR, Ka, Kx, gnu, L0):
        self.logR = np.array(logR, dtype=np.float, copy=True)
        self.Ka = np.array(Ka, dtype=np.float, copy=True)
        self.Kx = np.array(Kx*Ka[0], dtype=np.float, copy=True)
        self.gnu = np.array(gnu, dtype=np.int, copy=True)
        self.L0 = np.array(L0, dtype=np.float, copy=True)

        self.Req = reqSolver(self.logR, self.Ka, self.gnu, self.Kx, self.L0)

        self.vgridOut = StoneVgrid(np.power(10, self.Req), self.Ka, self.gnu, self.Kx, self.L0)
