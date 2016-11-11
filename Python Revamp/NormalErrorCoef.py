import numpy as np
from math import *
import loadData
import StoneMod
import pseudoNormlike

data = loadData.loadData()

## This function takes in a NumPy array of shape (12) for Rtot, the array KaMat from loadData, the array mfiAdjMean from loadData, the array
## tnpbsa from loadData, the array meanPerCond from loadData, and the array biCoefMat from loadData. The first six elements are the common
## logarithms of the recepter expression levels of FcgRIA, FcgRIIA-Arg, FcgRIIA-His, FcgRIIB, FcgRIIIA-Phe, and FcgRIIIA-Val (respectively),
## the common logarithm of the Kx coefficient (by which the affinity for any receptor-IgG combo is multiplied in order to return Kx), the common
## logarithms of the MFI-per-TNP-BSA ratios for TNP-4-BSA and TNP-26-BSA, respectively, the effective avidity of TNP-4-BSA, the effective avidity
## of TNP-26-BSA, and the coefficient by which the mean MFI for a certain combination of FcgR, IgG, and avidity is multiplied to produce the
## standard deviation of MFIs for that condition.
def NormalErrorCoef(Rtot,KaMat,mfiAdjMean,tnpbsa,meanPerCond,biCoefMat):
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
        L0 = tnpbsa[j]
        
        ## Iterate over each kind of FcgR
        for k in range(6):
            ## Set the common logarith of the level of receptor expression for the FcgR in question
            logR = Rtot[k]
            
            ## Iterate over each kind of IgG
            for l in range(4):
                ## Set the affinity for the binding of the FcgR and IgG in question
                Ka = KaMat[k][l]
                ## Calculate the Kx value for the combination of FcgR and IgG in question. Then, take the common logarithm of this value.
                Kx = 10**logKxcoef/Ka
                logKx = log10(Kx)
                ## Calculate the MFI which should result from this condition according to the model
                MFI = c*StoneMod.StoneMod(logR,Ka,v,logKx,L0,biCoefMat)

                ## Iterate over each real data point for this combination of TNP-BSA, FcgR, and IgG in question, calculating the log-likelihood
                ## of the point assuming the calculated point is true.
                temp = np.array([0.0]*4)
                for m in range(4):
                    temp[m] = mfiAdjMean[4*k+l][4*j+m]
                mean = meanPerCond[4*k+l][j]
                tempm = []
                for m in range(4):
                    tempm.append(pseudoNormlike.pseudoNormlike(temp[m], \
                                                                MFI,(sigCoef*mean)))
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

print(NormalErrorCoef([1]*12,data['kaBruhns'],data['mfiAdjMean'],data['tnpbsa'],data['meanPerCond'],data['biCoefMat']))
