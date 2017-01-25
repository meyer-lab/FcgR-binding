import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from StoneHelper import *


M, dset = read_chain('mcmc_chain.h5')

print(type(dset.as_matrix()))

bestIDX = np.argmax(dset['LL'])

p = dset.iloc[bestIDX,:][2:].as_matrix()
##print(list(dset[2]))
# Trim the burn in period
##dset = dset.iloc[300::,:]

dsett = dset.sort_values(by = 'LL')

##print(dset[[list(dset)[j] for j in range(7,len(list(dset)))]])
##dd = getFitPrediction(M,dset[[list(dset)[j] for j in range(7,len(list(dset)))]])


##print(dset.columns)

##dset = dset.assign(sigDiff = lambda x: np.power(10, x.sigConv2 - x.sigConv1))
##dset = dset.assign(gnuDiff = lambda x: x.gnu2 / x.gnu1)
##
##temp = getFitPrediction(M,dset)
frameList = mapMCMC(lambda x: getFitPrediction(M,x),dset.as_matrix()[:,2:])
frameAgg = reduceMCMC(frameList)
np.save('frameAgg',frameAgg)
