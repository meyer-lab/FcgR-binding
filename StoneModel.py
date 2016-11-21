import numpy as np
from loadData import *
from math import *
from scipy.optimize import bisect
from scipy.stats import norm

nan = float('nan')
inf = float('inf')

class StoneModel:
    ## The purpose of this function is to calculate the value of Req (from Equation 1 from Stone) given parameters R,
    ## kai=Ka,Li=L, vi=v, and kx=Kx. It does this by performing the bisction algorithm on Equation 2 from Stone. The
    ## bisection algorithm is used to find the value of log10(Req) which satisfies Equation 2 from Stone.
    def ReqFuncSolver(self, R, kai, Li, vi, kx):
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
        diffFunAnon = lambda x: self.diffFun(x,R,vi,kx,viLikdi)

        ## Implement the bisection algorithm using SciPy's bisect. Please see SciPy documentation for rationale behind
        ## input parameter not described beforehand.
        logReq = bisect(diffFunAnon,a,b,(),1e-12,np.finfo(float).eps*10,100,False,False)

        return logReq

    def diffFun(self, x, R, vi, kx, viLikdi):
        ## This function subtracts the right side of Equation 2 from Stone from the left side of the same Equation. The
        ## bisection algorithm is run using this function so as to calculate log10(Req) which satisfies all parameters.

        ## Each time this function is called: x is log10 of the value of Req being tested, R is R from Stone 2, vi is v from
        ## Stone 2, kx is Kx from Stone 2, and viLikdi is a product which is constant over all iterations of the bisection
        ## algorithm over diffFun for a single calling of ReqFuncSolver.
        x = 10**x
        diff = R-x*(1+viLikdi*(1+kx*x)**(vi-1))
        return diff

    def StoneMod(self,logR,Ka,v,logKx,L0,biCoefMat):
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
        v = np.int_(v)

        ## Vector of binomial coefficients
        biCoefVec = biCoefMat[v-1][0:v]
        Req = 10**self.ReqFuncSolver(R,Kd,L0,v,Kx)
        if isnan(Req):
            return -1e50

        ## Calculate L, according to equations 1 and 7
        Lpre = 0
        for j in range(v):
            Lpre = Lpre+biCoefVec[j]*Kx**j*Req**(j+1)
        L = Lpre*L0/Kd

        return L

    ## This function takes in a NumPy array of shape (12) for Rtot, the array KaMat from loadData, the array mfiAdjMean from loadData, the array
    ## tnpbsa from loadData, the array meanPerCond from loadData, and the array biCoefMat from loadData. The first six elements are the common
    ## logarithms of the recepter expression levels of FcgRIA, FcgRIIA-Arg, FcgRIIA-His, FcgRIIB, FcgRIIIA-Phe, and FcgRIIIA-Val (respectively),
    ## the common logarithm of the Kx coefficient (by which the affinity for any receptor-IgG combo is multiplied in order to return Kx), the common
    ## logarithms of the MFI-per-TNP-BSA ratios for TNP-4-BSA and TNP-26-BSA, respectively, the effective avidity of TNP-4-BSA, the effective avidity
    ## of TNP-26-BSA, and the coefficient by which the mean MFI for a certain combination of FcgR, IgG, and avidity is multiplied to produce the
    ## standard deviation of MFIs for that condition.
    def NormalErrorCoef(self, Rtot):
        ## Set the standard deviation coefficient
        sigCoef = 10**Rtot[11]

        ## Set thecommon logarithm of the Kx coefficient
        logKxcoef = Rtot[6]
        logSqrErrMatPre0 = []
        logSqrErrMatPre1 = []

        ## Iterate over each kind of TNP-BSA (4 or 26)
        for j in range(2):
            ## Set the effective avidity for the kind of TNP-BSA in question
            v = Rtot[9+j]
            ## Set the MFI-per-TNP-BSA conversion ratio for the kind of TNP-BSA in question
            c = 10**Rtot[7+j]
            ## Set the ligand (TNP-BSA) concentration for the kind of TNP-BSA in question
            L0 = self.tnpbsa[j]

            ## Iterate over each kind of FcgR
            for k in range(6):
                ## Set the common logarith of the level of receptor expression for the FcgR in question
                logR = Rtot[k]

                ## Iterate over each kind of IgG
                for l in range(4):
                    ## Set the affinity for the binding of the FcgR and IgG in question
                    Ka = self.kaBruhns[k][l]
                    ## Calculate the Kx value for the combination of FcgR and IgG in question. Then, take the common logarithm of this value.
                    Kx = 10**logKxcoef/Ka
                    logKx = log10(Kx)
                    ## Calculate the MFI which should result from this condition according to the model
                    MFI = c*self.StoneMod(logR,Ka,v,logKx,L0,self.biCoefMat)

                    ## Iterate over each real data point for this combination of TNP-BSA, FcgR, and IgG in question, calculating the log-likelihood
                    ## of the point assuming the calculated point is true.
                    temp = np.array([0.0]*4)
                    for m in range(4):
                        temp[m] = self.mfiAdjMean[4*k+l][4*j+m]
                    mean = self.meanPerCond[4*k+l][j]
                    tempm = []
                    for m in range(4):
                        tempm.append(norm.logpdf(temp[m], MFI, (sigCoef*mean)))
                    tempm = np.array(tempm)

                    ## For each TNP-BSA, have an array which includes the log-likelihoods of all real points in comparison to the calculated values.
                    if j == 0:
                        logSqrErrMatPre0 = np.concatenate((logSqrErrMatPre0,tempm))
                    else:
                        logSqrErrMatPre1 = np.concatenate((logSqrErrMatPre1,tempm))

        ## Concatenate the arrays logSqrErrMatPre0 and logSqrErrMatPre1 to form logSqrErrMat
        logSqrErrMat = np.concatenate((logSqrErrMatPre0,logSqrErrMatPre1),0)
        ## Calculate the log-likelihood of the entire set of parameters by summing all the calculated log-likelihoods.
        logSqrErr = 0
        for elem in logSqrErrMat:
            logSqrErr = logSqrErr+np.nansum(elem)
        return logSqrErr

    def __init__(self):
        self.data = loadData()

        self.biCoefMat = self.data['biCoefMat']
        self.kaBruhns = self.data['kaBruhns']
        self.mfiAdjMean = self.data['mfiAdjMean']
        self.meanPerCond = self.data['meanPerCond']
        self.tnpbsa = self.data['tnpbsa']
