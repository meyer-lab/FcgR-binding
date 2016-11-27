import numpy as np
import matlab.engine
from loadData import loadData
###########################################################################
## Checking the data produced by the Python function loadData against the
## original MATLAB function loadData. This script interfaces with both the
## Python script loadData and with the MATLAB function loadDataINTERFACE.
## The NumPy array biCoefMat and the MATLAB matrix biCoefMat have previously
## been proven to be equal, and so this fact will not be checked in this
## script. All other parameters will be calculated in both MATLAB and Python
## and then checked against each other to check for any disparity.
###########################################################################

## Procure all of the data from the Python function loadData
data = loadData()

mfiAdjMean = data['mfiAdjMean']
tnpbsa = data['tnpbsa']
kaBruhns = data['kaBruhns']
meanPerCond = data['meanPerCond']

## Initialize MATLAB engine. 
eng = matlab.engine.start_matlab()

## Compare mfiAdjMean between both loadData functions. Note that mfiAdjMean 
mfiAdjMeanMAT = eng.loadDataINTERFACE(1.0)

print(mfiAdjMean.shape)
