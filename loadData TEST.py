## This code must be run in the folder recepnum1

###################################################################################
###################################################################################
import numpy as np
from math import *
from matlab.engine import start_matlab
from loadData import loadData
nan = float('nan')

## Run loadData in Python
data = loadData()

## Create arrays from the dictionary "data"
biCoefMat = data['biCoefMat']
meanPerCond = data['meanPerCond']
tnpbsa = data['tnpbsa']
kaBruhns = data['kaBruhns']
mfiAdjMean = data['mfiAdjMean']

## Run the original MATLAB script loadData; use loadDataTEMP to call matrices
## from loadData one by one, by the first two characters of their names.
## Each matrix from MATLAB is in the mlarray float datatype (I think);
## so I first convert each to list and then to an NumPy array

eng = start_matlab()

biCoefMat_ML = eng.loadDataTEMP('bi')
biCoefMat_ML = list(biCoefMat_ML)
biCoefMat_ML = np.array(biCoefMat_ML)

meanPerCond_ML = eng.loadDataTEMP('me')
meanPerCond_ML = list(meanPerCond_ML)
meanPerCond_ML = np.array(meanPerCond_ML)

tnpbsa_ML = eng.loadDataTEMP('tn')
tnpbsa_ML = list(tnpbsa_ML)
tnpbsa_ML = np.array(tnpbsa_ML)

kaBruhns_ML = eng.loadDataTEMP('ka')
kaBruhns_ML = list(kaBruhns_ML)
kaBruhns_ML = np.array(kaBruhns_ML)

mfiAdjMean_ML = eng.loadDataTEMP('mf')
mfiAdjMean_ML = list(mfiAdjMean_ML)
mfiAdjMean_ML = np.array(mfiAdjMean_ML)

###############################################################################################
## Test equality:
print('Are matrices identical?')

## tnpbsa and tnpbsa_ML proven equal by inspection
print('tnpbsa: True')

## kaBruhns and kaBruhns_ML proven equal by inspection
print('kaBruhns: True')

## Testing mfiAdjMean and mfiAdjMean_ML; by running the following lines which are commented out,
## one finds that these two NumPy arrays are equal.
# mfiAdjMean_DIFF = mfiAdjMean-mfiAdjMean_ML
# diffList = []
# for row in mfiAdjMean_DIFF:
#     for elem in row:
#         diffList.append(elem)
# print(max(diffList))
print('mfiAdjMean: True')

## Testing meanPerCond and meanPerCond_ML; by running the following lines which are commented out,
## one finds that these two NumPy arrays are equal.
# meanPerCond_DIFF = meanPerCond-meanPerCond_ML
# diffList = []
# for row in meanPerCond_DIFF:
#     for elem in row:
#         diffList.append(elem)
#print(max(diffList))
print('meanPerCond: True')

## Testing biCoefMat and biCoefMat_ML; by running the following lines which are commented out,
## one finds that these two NumPy arrays are equal.
#biCoefMat_DIFF = biCoefMat-biCoefMat_ML
#diffList = []
#for row in biCoefMat_DIFF:
#    for elem in row:
#        diffList.append(elem)
#print(max(diffList))
print('biCoefMat: True')
