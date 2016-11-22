from math import *
from emcee import EnsembleSampler
import numpy as np
import StoneModel
import csv
import time
import sys
import h5py

newData = 1
bestLL = -inf

###########################################################
## Load model
StoneM = StoneModel.StoneModel()
###########################################################

## Upper and lower bounds of the 12 parameters
lbR = 0
ubR = 8
lbKx = -10
ubKx = 0
lbc = -10
ubc = 5
lbv = 1
ubv = 30
lbsigma = -10
ubsigma = 2

## Create vectors for upper and lower bounds
if newData:
    lb = np.array([lbKx,lbc,lbc,lbv,lbv,lbsigma])
    ub = np.array([ubKx,ubc,ubc,ubv,ubv,ubsigma])
else:
    lb = np.array([lbR,lbR,lbR,lbR,lbR,lbR,lbKx,lbc,lbc,lbv,lbv,lbsigma])
    ub = np.array([ubR,ubR,ubR,ubR,ubR,ubR,ubKx,ubc,ubc,ubv,ubv,ubsigma])


## Create function for the running of the MCMC
def loglF(x):
    if np.any(np.isinf(x)) or np.any(np.isnan(x)) or np.any(np.less(x, lb)) or np.any(np.greater(x, ub)):
        return -float('inf')

    if newData:
        x[3:5] = np.floor(x[3:5])
        output = StoneM.NormalErrorCoefRset(x)
    else:
        x[9:11] = np.floor(x[9:11])
        output = StoneM.NormalErrorCoef(x)

    return(output)

#### Run simulation
niters = 100000

## Set up parameters for parallel-tempered Ensemble Sampler
ndims, nwalkers = int(np.size(lb)), 100
p0 = np.random.uniform(low=0, high=1, size=(nwalkers, ndims))

for ii in range(0, nwalkers):
    p0[ii] = lb + (ub - lb)*p0[ii]

## Set up sampler
sampler = EnsembleSampler(nwalkers,ndims,loglF,2.0,[],{},None,16)

f = h5py.File("mcmc_chain.h5", 'w', libver='latest')
dset = f.create_dataset("data", chunks=True, maxshape=(None, len(lb) + 2), data=np.ndarray((0, len(lb) + 2)))
f.swmr_mode = True
thinTrack = 1
thin = 10

for p, lnprob, lnlike in sampler.sample(p0, iterations=niters, storechain=False):
    if thinTrack < thin:
        thinTrack += 1
    else:
        if np.max(lnprob) > bestLL:
            bestLL = np.max(lnprob)

        matOut = np.concatenate((lnprob.reshape(nwalkers, 1), np.arange(0, nwalkers).reshape(nwalkers, 1), p.reshape(nwalkers, ndims)), axis=1)

        fShape = dset.shape
        dset.resize((fShape[0] + np.shape(matOut)[0], fShape[1]))
        dset[fShape[0]:, :] = matOut
        f.flush()

        print((fShape, bestLL))
        thinTrack = 1
    pass
