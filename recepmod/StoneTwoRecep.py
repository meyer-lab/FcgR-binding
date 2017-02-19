import numpy as np
from scipy.optimize import brentq
from scipy.misc import comb
from memoize import memoize

# A fast cached version of nchoosek
@memoize
def nmultichoosek(n, k, i):
    return comb(n, k, exact=True)*comb(n-k, i, exact=True)

# This function takes in the relevant parameters and creates the v_ij grid
# Kx should be the Kx of Ka[0]
# Ka should be a tuple of size 2 with each affinity
# Req should be a tuple of size 2
def StoneVgrid(Req,Ka,gnu,Kx,L0):
    # Initialize the grid of possibilities
    vGrid = np.zeros([gnu+1, gnu+1], dtype = np.float64)

    # ii is the number of receptor one bound
    for ii in range(gnu+1):
        # jj is the number of receptor two bound
        for jj in range(gnu+1):
            if ii+jj > gnu or (ii == 0 and jj == 0):
                continue

            nmk = L0 * nmultichoosek(gnu,ii,jj)

            ReqPenalty = Req[0]**ii * Req[1]**jj

            KxPenalty = Kx**(ii+jj-1) * (Ka[1]/Ka[0])**jj

            vGrid[ii, jj] = Ka[0]*nmk*KxPenalty*ReqPenalty

    return vGrid

# This calculates the Rbnd quantity from a v_ij grid
def StoneRbnd(vGrid):
    # We can calculate gnu from the size of the v_ij grid
    gnu = vGrid.shape[0] - 1

    # Sum along each axis to get the number of receptors in each pool
    vGridSone = np.sum(vGrid, axis = 1)
    vGridStwo = np.sum(vGrid, axis = 0)

    # Multiply by number of receptors in each case
    vGridSone = np.multiply(vGridSone, np.arange(gnu+1))
    vGridStwo = np.multiply(vGridStwo, np.arange(gnu+1))

    return np.array((np.sum(vGridSone), np.sum(vGridStwo)))

# This calculates the RmultiAll quantity from a v_ij grid
# This is the number of receptors multimerized with self or non-self
def StoneRmultiAll(vGrid):
    vGrid = np.copy(vGrid)

    # We can calculate gnu from the size of the v_ij grid
    gnu = vGrid.shape[0] - 1

    # Erase species that are bound all on their own
    vGrid[1,0] = 0.0
    vGrid[0,1] = 0.0

    # Sum along each axis to get the number of receptors in each pool
    vGridSone = np.sum(vGrid, axis = 1)
    vGridStwo = np.sum(vGrid, axis = 0)

    # Multiply by number of receptors in each case
    vGridSone = np.multiply(vGridSone, np.arange(gnu+1))
    vGridStwo = np.multiply(vGridStwo, np.arange(gnu+1))

    return np.array((np.sum(vGridSone), np.sum(vGridStwo)))

# Solve for Req
def reqSolver(logR,Ka,gnu,Kx,L0):
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

    curReq = np.array((-40, -40), dtype = np.float64)
    prevReq = np.array(curReq, copy = True)

    if np.max(np.multiply(rootF(curReq),rootF(logR))) > 0:
        return np.array([np.nan, np.nan], dtype = np.float64)

    # The two receptors only weakly interact, so try and find the roots separately in an iterive fashion
    for ii in range(50):
        curReq[1] = brentq(lambda x: rootF(np.array((curReq[0], x)))[1], -40, logR[1], disp=False)
        curReq[0] = brentq(lambda x: rootF(np.array((x, curReq[1])))[0], -40, logR[0], disp=False)

        if np.max(np.abs(rootF(curReq))) < 1.0E-6 and ii > 3 and np.max(np.abs(curReq - prevReq)) < 1E-6:
            return curReq
        else:
            prevReq = curReq

    return np.array([np.nan, np.nan], dtype = np.float64)

class StoneTwo:
    def getRbnd(self, gnu, L0):
        Req = reqSolver(self.logR,self.Ka,gnu,self.Kx,L0)

        vgridOut = StoneVgrid(np.power(10,Req),self.Ka,gnu,self.Kx,L0)

        return StoneRbnd(vgridOut)

    def getRmultiAll(self, gnu, L0):
        Req = reqSolver(self.logR,self.Ka,gnu,self.Kx,L0)

        vgridOut = StoneVgrid(np.power(10,Req),self.Ka,gnu,self.Kx,L0)

        return StoneRmultiAll(vgridOut)

    def __init__(self, logR, Ka, Kx):
        self.logR = np.array(logR, dtype=np.float64, copy=True)
        self.Ka = np.array(Ka, dtype=np.float64, copy=True)
        self.Kx = np.array(Kx, dtype=np.float64, copy=True)
