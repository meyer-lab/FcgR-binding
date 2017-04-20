import recepmod.StoneHelper as sh
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

M, dset = sh.read_chain('recepmod/data/test_chain.h5')
##M, dset = read_chain(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_chain.h5"))

##dsett = dsett.T.rename(index=[dsett.T[j].loc[['walker']] for j in dsett.T.columns],columns=dsett.T.columns)
##dsett = dsett.T
##
##dsett.columns = [item % 52 for item in dsett.columns]
S, P = sh.geweke_chains(dset)

def temp(dset):
    print('Pre-alteration:')
    print(dset)
    nwalkers = int(np.max(dset['walker']))+1
    dsett = dset.T
    print('Transpose:')
    print(dsett)
    dsett.columns = [item % nwalkers for item in dsett.columns]
    for j in range(2):
        print(dsett[j].T)

##temp(dset)
Statistics, Pvalues = sh.geweke_chains(dset)
##print(len(Statistics))
##print('\n')
##print(len(Statistics[0]))
nwalkers = len(Pvalues)
axx = []
for j in range(13):
    axx.append(plt.subplot(5,3,j+1))
    temp = []
    for item in Pvalues:
        temp.append(item[j])
    temp = np.array(temp)
    axx[j].hist(temp)
plt.show()
