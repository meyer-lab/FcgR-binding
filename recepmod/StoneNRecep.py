import numpy as np
import pandas as pd

def StoneVgrid(Req,Ka,gnu,Kx,L0):
    """
    This function takes in the relevant parameters and creates the v_ij grid
    Kx should be the Kx of Ka[0]
    Ka should be a tuple of size 2 with each affinity
    Req should be a tuple of size 2
    """
    from .StoneModel import nchoosek1

    if len(Req) != len(Ka):
        raise IndexError("Req and Ka must be same length.")

    # Initialize the grid of possibilities
    vGrid = np.zeros(np.full((len(Req),), gnu+1), dtype=np.float)

    # ii, jj is the number of receptor one, two bound
    it = np.nditer(vGrid, flags=['multi_index'])

    while not it.finished:
        cur_pos = it.multi_index

        if sum(cur_pos) <= gnu and sum(cur_pos) > 0:
        	vGrid[cur_pos] = L0 * Ka[0] / Kx * nchoosek1(gnu, sum(cur_pos))

        	for ii in range(len(Req)):
        		vGrid[cur_pos] *= np.power(Ka[ii]/Ka[0]*Req[ii]*Kx, cur_pos[ii])

        	for ii in range(1, len(Req)):
        		vGrid[cur_pos] *= nchoosek1(sum(cur_pos), sum(cur_pos[0:ii]))

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

    def __init__(self, logR, Ka, Kx, gnu, L0):
        self.logR = np.array(logR, dtype=np.float64, copy=True)
        self.Ka = np.array(Ka, dtype=np.float64, copy=True)
        self.Kx = np.array(Kx*Ka[0], dtype=np.float64, copy=True)
        self.gnu = np.array(gnu, dtype=np.int, copy=True)
        self.L0 = np.array(L0, dtype=np.float64, copy=True)

        self.Req = reqSolver(self.logR, self.Ka, self.gnu, self.Kx, self.L0)

        self.vgridOut = StoneVgrid(np.power(10, self.Req), self.Ka, self.gnu, self.Kx, self.L0)















