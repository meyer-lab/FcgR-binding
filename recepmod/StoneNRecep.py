import numpy as np
import pandas as pd
from .StoneModel import nchoosek


#@profile
def StoneVgrid(Req,Ka,gnu,Kx,L0):
    """
    This function takes in the relevant parameters and creates the v_ij grid
    Kx should be the Kx of Ka[0]
    Ka should be a tuple of size N with each affinity
    Req should be a tuple of size N
    """

    if len(Req) != len(Ka):
        raise IndexError("Req and Ka must be same length.")

    # Initialize the grid of possibilities
    vGrid = np.zeros(np.full((len(Req),), gnu+1), dtype=np.float)

    # Precalculate outside terms
    vGridBegin = L0 * Ka[0] / Kx * nchoosek(gnu)
    KKRK = np.multiply(Ka, Req)/Ka[0]*Kx

    # ii, jj is the number of receptor one, two bound
    it = np.nditer(vGrid, flags=['multi_index'])

    while not it.finished:
        cur_pos = it.multi_index
        scur = sum(cur_pos)

        if scur <= gnu and scur > 0:
            vGrid[cur_pos] = vGridBegin[scur] * np.power(KKRK, cur_pos).prod()
            
            if len(Req) > 2 and scur > cur_pos[0]:
                vGrid[cur_pos] *= nchoosek(scur)[np.cumsum(cur_pos)[1:]].prod()

        it.iternext()

    return vGrid


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

    vGrid = np.copy(vGrid)

    # Erase species that are bound all on their own
    for ii in range(len(vGrid.shape)):
        idx = np.zeros((len(vGrid.shape), ), dtype=np.int)
        idx[ii] = 1

        vGrid[idx] = 0.0

    # Just Rbnd from here
    return StoneRbnd(vGrid)


def reqSolver(logR,Ka,gnu,Kx,L0):
    """ Solve for Req """
    from scipy.optimize import brentq

    failV = np.full(logR.shape, np.nan, dtype=np.float64)

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

    curReq = np.full(logR.shape, -40, dtype = np.float64)
    prevReq = curReq.copy()

    if np.max(np.multiply(rootF(curReq), rootF(logR))) > 0:
        return failV

    # The two receptors only weakly interact, so try and find the roots separately in an iterive fashion
    for ii in range(50):
        for jj in range(len(curReq)):
            curReq[jj] = brentq(lambda x: overF(curReq, jj, x), -40, logR[jj], disp=False)

        if np.max(np.abs(rootF(curReq))) < 1.0E-6 and ii > 3 and np.max(np.abs(curReq - prevReq)) < 1E-6:
            return curReq
        else:
            prevReq = curReq

    return failV


def activityBias(vGrid):
    vGrid = np.copy(vGrid)

    # We can calculate gnu from the size of the v_ij grid
    gnu = vGrid.shape[0] - 1

    activity = 0.0

    # ii, jj is the number of receptor one, two bound
    it = np.nditer(vGrid, flags=['multi_index'])

    while not it.finished:
        cur_pos = it.multi_index

        for jj in range(len(cur_pos)):
            if jj == 1:
                sign = -1.0
            else:
                sign = 1.0

            activity += sign * np.fmax(vGrid[cur_pos] * (cur_pos[jj]-1), 0.0)

        it.iternext()

    return activity


class StoneN:
    def getRbnd(self):
        return StoneRbnd(self.vgridOut)

    def getRmultiAll(self):
        return StoneRmultiAll(self.vgridOut)

    def getActivity(self):
        return activityBias(self.vgridOut)

    def getActBnd(self):
        """ TODO: Define this quantity in a rigorous fashion. """
        outt = StoneRbnd(self.vgridOut)

        return np.log(np.fmax(np.sum(outt) - 2*outt[1], 1.0))

    def getAllProps(self):
        return pd.Series(dict(ligand = self.L0,
                              avidity = self.gnu,
                              ligandEff = self.L0*self.gnu,
                              Kx = self.Kx), dtype = np.float64)


    def __init__(self, logR, Ka, Kx, gnu, L0):
        self.logR = np.array(logR, dtype=np.float64, copy=True)
        self.Ka = np.array(Ka, dtype=np.float64, copy=True)
        self.Kx = np.array(Kx*Ka[0], dtype=np.float64, copy=True)
        self.gnu = np.array(gnu, dtype=np.int, copy=True)
        self.L0 = np.array(L0, dtype=np.float64, copy=True)

        self.Req = reqSolver(self.logR, self.Ka, self.gnu, self.Kx, self.L0)

        self.vgridOut = StoneVgrid(np.power(10, self.Req), self.Ka, self.gnu, self.Kx, self.L0)
