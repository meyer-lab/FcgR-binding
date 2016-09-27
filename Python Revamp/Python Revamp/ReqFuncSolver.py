from math import *
import loadData

data = loadData.loadData()


def ReqFuncSolver(R, kai, Li, vi, kx):
    kdi = 1/kai
    viLikdi = vi*Li/kdi

    a = -20
    b = log10(R)

    bVal = diffFun(b,R,vi,kx,viLikdi)
    cVal = diffFun(a,R,vi,kx,viLikdi)

    ## Is there no root within the interval?
    if bVal*cVal > 0:
        c = 1000
        return c
    
    ## In the case that (b - a > 1e-4 || abs(cVal) > 1e-4) == 1 to begin
    ## with; only implemented for MATLAB Coder
    c = 1000
    ## Commence algorithm
    while ((b - a > 1e-4) and (abs(cVal) > 1e-4)):
        c = (a+b)/2
        cVal = diffFun(c, R, vi, kx, viLikdi)
        
        if cVal*bVal >= 0:
            b = c
            bVal = cVal
        else:
            a = c
    return c

def diffFun(x, R, vi, kx, viLikdi):
    x = 10**x
    diff = R-x*(1+viLikdi*(1+kx*x)**(vi-1))
    return diff

print(ReqFuncSolver(1000,data['kaBruhns'][0,0],data['tnpbsa'][0],26,1e-10))
