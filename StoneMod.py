import numpy as np
from ReqFuncSolver import *
from loadData import *
from math import *

data = loadData()

def StoneMod(logR,Ka,v,logKx,L0,biCoefMat):
    ## Returns the number of mutlivalent ligand bound to a cell with 10^logR
    ## receptors, granted each epitope of the ligand binds to the receptor
    ## kind in question with dissociation constant Kd and cross-links with
    ## other receptors with crosslinking constant Kx = 10^logKx. All
    ## equations derived from Stone et al. (2001). Assumed that ligand is at
    ## saturating concentration L0 = 7e-8 M, which is as it is (approximately)
    ## for TNP-4-BSA in Lux et al. (2013).
    Kd = 1/Ka
    Kx = 10**logKx
    R = 10**logR
    
    ## Vector of binomial coefficients
    biCoefVec = biCoefMat[v-1][0:v]
    Req = 10**ReqFuncSolver(R,Kd,L0,v,Kx)
    
    ## Calculate L, according to equations 1 and 7
    Lpre = 0
    for j in range(v):
        Lpre = Lpre+biCoefVec[j]*Kx**j*Req**(j+1)
    L = Lpre*L0/Kd
    
    return L
