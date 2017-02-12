import numpy as np
from scipy.optimize import brentq
from scipy.misc import comb
from memoize import memoize
import pandas as pd

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
            if ii+jj > gnu:
                continue

            nmk = L0 * nmultichoosek(gnu,ii,jj)
            ReqPenalty = Req[0]**jj * Req[1]**ii

            if ii > 0:
                KxPenalty = Kx**(ii+jj-1) * (Ka[1]/Ka[0])**jj
                vGrid[ii, jj] = Ka[0]*nmk*KxPenalty*ReqPenalty
            elif jj > 0:
                KxPenalty = Kx**(ii+jj-1) * (Ka[1]/Ka[0])**(jj-1)
                vGrid[ii, jj] = Ka[1]*nmk*KxPenalty*ReqPenalty

    return vGrid

# This calculates the Rbnd quantity from a v_ij grid
def StoneRbnd(vGrid):
    # We can calculate gnu from the size of the v_ij grid
    gnu = vGrid.shape[0] - 1

    # Sum along each axis to get the number of receptors in each pool
    vGridSone = np.sum(vGrid, axis = 0)
    vGridStwo = np.sum(vGrid, axis = 1)

    # Multiply by number of receptors in each case
    vGridSone = np.multiply(vGridSone, np.arange(gnu+1))
    vGridStwo = np.multiply(vGridStwo, np.arange(gnu+1))

    return np.array((np.sum(vGridSone), np.sum(vGridStwo)))

# This calculates the Rbnd quantity from a v_ij grid
def StoneRbndDist(vGrid):
    # We can calculate gnu from the size of the v_ij grid
    gnu = vGrid.shape[0] - 1

    # Sum along each axis to get the number of receptors in each pool
    vGridSone = np.sum(vGrid, axis = 0)
    vGridStwo = np.sum(vGrid, axis = 1)

    # Multiply by number of receptors in each case
    vGridSone = np.multiply(vGridSone, np.arange(gnu+1))
    vGridStwo = np.multiply(vGridStwo, np.arange(gnu+1))

    return (vGridSone, vGridStwo)

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

    # The two receptors only weakly interact, so try and find the roots separately in an iterive fashion
    for ii in range(5):
        curReq[0] = brentq(lambda x: rootF(np.array((x, curReq[1])))[0], -40, logR[0], disp=False)
        curReq[1] = brentq(lambda x: rootF(np.array((curReq[0], x)))[1], -40, logR[1], disp=False)

        if np.max(rootF(curReq)) < 2.0E-12:
            return curReq

    return np.array([np.nan, np.nan], dtype = np.float64)

class StoneTwo:
    def __init__(self):
        print("Starting up")


if __name__ == "__main__":
    M = StoneTwo()

    Kd = 1.0E-8
    L = 1E-7
    Kx = 1.0E-7

    logR = np.array((3, 2), dtype = np.float64)

    Req = reqSolver(logR, 1/Kd, 9, Kx, L)

    gridd = StoneVgrid(np.power(10, Req), 1/Kd, 9, Kx, L)

    Rbnd = StoneRbndDist(gridd)

    np.set_printoptions(precision=1, linewidth=125)

    print(Rbnd[0])
    print(Rbnd[1])
