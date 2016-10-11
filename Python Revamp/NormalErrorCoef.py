import numpy as np
from math import *
import loadData
import StoneMod
import pseudoNormlike

data = loadData.loadData()

def NormalErrorCoef(Rtot,KaMat,mfiAdjMean,tnpbsa,meanPerCond,biCoefMat):
    sigCoef = 10**Rtot[11]
    logKxcoef = Rtot[6]

    logSqrErrMatPre0 = []
    logSqrErrMatPre1 = []
    for j in range(2):
        v = Rtot[9+j]
        c = 10**Rtot[7+j]
        L0 = tnpbsa[j]
        for k in range(6):
            logR = Rtot[k]
            print('Initial logR: '+str(logR))
            for l in range(4):
                Ka = KaMat[k][l]
                Kx = 10**logKxcoef/Ka
                logKx = log10(Kx)
                MFI = c*StoneMod.StoneMod(logR,Ka,v,logKx,L0,biCoefMat)
                temp = np.array([0]*4)
                for m in range(4):
                    temp[m] = mfiAdjMean[4*k+l][4*j+m]
                mean = meanPerCond[4*k+l][j]
                tempm = []
                for m in range(4):
                    tempm.append(pseudoNormlike.pseudoNormlike(temp[m], \
                                                                MFI,(sigCoef*mean)))
                tempm = np.array(tempm)
                if j == 0:
                    logSqrErrMatPre0 = np.concatenate((logSqrErrMatPre0,tempm))
                else:
                    logSqrErrMatPre1 = np.concatenate((logSqrErrMatPre1,tempm))
                
    logSqrErr = 0
    for elem in logSqrErrMat:
        logSqrErr = logSqrErr+np.nansum(elem)
    return logSqrErr

print(NormalErrorCoef([1]*12,data['kaBruhns'],data['mfiAdjMean'],data['tnpbsa'],data['meanPerCond'],data['biCoefMat']))
