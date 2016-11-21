import numpy as np
from math import *
from loadData import loadData

data = loadData()

biCoefMat = data['biCoefMat']
kaBruhns = data['kaBruhns']
mfiAdjMean = data['mfiAdjMean']
meanPerCond = data['meanPerCond']

nan = float('nan')
inf = float('inf')

def StoneMod(logR,Ka,v,logKx,L0,biCoefMat):
    ## Returns the number of mutlivalent ligand bound to a cell with 10^logR
    ## receptors, granted each epitope of the ligand binds to the receptor
    ## kind in question with dissociation constant Kd and cross-links with
    ## other receptors with crosslinking constant Kx = 10^logKx. All
    ## equations derived from Stone et al. (2001).
    
    ####################################################################################
    ## Convert Ka to Kd for similarity to original MATLAB script. Create Kx from logKx and R from logR
    Kd = 1/Ka
    Kx = 10**logKx
    R = 10**logR
    
    ## Vector of binomial coefficients from biCoefMat; to avoid computation of n choose k in equation 1 from Stone 2001
    biCoefVec = biCoefMat[v-1][0:v]
    logReq = ReqFuncSolver(R,Kd,L0,v,Kx)
    if isnan(logReq):
        return -1e50
    Req = 10**ReqFuncSolver(R,Kd,L0,v,Kx)
    
    ## Calculate L, according to equations 1 and 7
    L = 0
    for j in range(int(v)):
        L = L+biCoefVec[j]*Kx**j*Req**(j+1)

    ##************************************************************************************************************
    ## Return the sum of all values L from equation 1 which are pertinent according to equation 7
    return L*L0/Kd

def ReqFuncSolver(R, kai, Li, vi, kx):
    ## The purpose of this function is to solver for Req in equation 2 in Stone 2001. This function,
    ## a bisection solver, is necessary for that there does not exist an algebraic solution for Req
    ## in equation 2 from Stone.

    ######################
    ## Convert Ka to Kd for ease of writing this function, and for similarity with original MATLAB function
    kdi = 1/kai
    ## viLikdi is a constant used frequently in this bisection algorithm; to save runtime, it is calculated
    ## once here.
    viLikdi = vi*Li/kdi

    ## a is the lower bound of the bisection;
    ## b is the upper bound of the bisection.
    a = -20
    b = log10(R)
##    print(a)
##    print(b)
##    print(' ')

    ## This algorithm works by generating a value c between a and b at each step and finding whether the solution
    ## is above or below c. After determining which, a new a and b are generated using the pre-existing a, b, and c,
    ## and the algorithm continues. bVal the initial value of the function diffFun at x = b, and cVal is the intial
    ## value of the function diffFun at x = a.
    bVal = diffFun(b,R,vi,kx,viLikdi)
    cVal = diffFun(a,R,vi,kx,viLikdi)
##    print(bVal)
##    print(cVal)

    ## Is there no root within the interval?
    if bVal*cVal > 0:
        c = nan
        return c
    
    ## In the case that (b - a > 1e-4 and abs(cVal) > 1e-4) == 1 to begin with.
    c = nan
    ## Commence algorithm; please see description of algortith above. Note that this bisection algorithm is being used
    ## to find the common logarithm of Req and not Req directly.
    while ((b - a > 1e-4) and (abs(cVal) > 1e-4)):
        c = (a+b)/2
##        print(str(bVal)+'     '+str(cVal))
        cVal = diffFun(c, R, vi, kx, viLikdi)
        
        if cVal*bVal >= 0:
            b = c
            bVal = cVal
        else:
            a = c

    return c

    ######################

def diffFun(x, R, vi, kx, viLikdi):
    ## The function by which the bisection algorithm gauges convergence. The closer the value of diffFun to 0, the closer
    ## x is to the common logarithm of Req.
    x = 10**x
    diff = R-x*(1+viLikdi*(1+kx*x)**(vi-1))
    return diff

print(StoneMod(8,1e-6,4,-8,7e-6,biCoefMat))
