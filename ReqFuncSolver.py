## The purpose of this function is to calculate the value of Req (from Equation 1 from Stone) given parameters R,
## kai=Ka,Li=L, vi=v, and kx=Kx. It does this by performing the bisction algorithm on Equation 2 from Stone. The
## bisection algorithm is used to find the value of log10(Req) which satisfies Equation 2 from Stone.

from math import *
import numpy as np
from scipy.optimize import bisect
import loadData

## Call all parameters from the Nimmerjahn Lab's data, as well as pertinent auxiliary parameters
data = loadData.loadData()

def ReqFuncSolver(R, kai, Li, vi, kx):
    ## Calculate kdi from kai for the sake of maintaining similarity to the original MATLAB function; kdi=Kd, Kd being
    ## Kd as used in Equation 2 from Stone.
    kdi = 1/kai
    ## Caculate the product vi*Li/kdi, which is used in Equation 2 from Stone and which is constant for all iterations
    ## of the bisection algorithm on diffFun (Equation 2 from Stone) for a given calling of ReqFuncSolver.
    viLikdi = vi*Li/kdi

    ## a is the lower bound for log10(Req) bisecion. By Equation 2, log10(Req) is necessarily lower than log10(R).
    a = -20
    b = log10(R)

    ## Create anonymous function diffFunAnon which calls diffFun for parameters R, vi=v, kx=Kx, and viLikdi.
    diffFunAnon = lambda x: diffFun(x,R,vi,kx,viLikdi)
    
    ## Implement the bisection algorithm using SciPy's bisect. Please see SciPy documentation for rationale behind
    ## input parameter not described beforehand.
    logReq = bisect(diffFunAnon,a,b,(),1e-12,np.finfo(float).eps*10,100,False,False)

    return logReq

def diffFun(x, R, vi, kx, viLikdi):
    ## This function subtracts the right side of Equation 2 from Stone from the left side of the same Equation. The
    ## bisection algorithm is run using this function so as to calculate log10(Req) which satisfies all parameters.

    ## Each time this function is called: x is log10 of the value of Req being tested, R is R from Stone 2, vi is v from
    ## Stone 2, kx is Kx from Stone 2, and viLikdi is a product which is constant over all iterations of the bisection
    ## algorithm over diffFun for a single calling of ReqFuncSolver.
    x = 10**x
    diff = R-x*(1+viLikdi*(1+kx*x)**(vi-1))
    return diff
