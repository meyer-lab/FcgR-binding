from math import *
from emcee import EnsembleSampler
import numpy as np
import StoneModel
import csv
import time
import sys
import h5py

## Define best
best = np.array([5.7204,5.658,5.9681,5.8991,4.8384,6.1420,-6.8541,-5.7668,-5.5631,7.0,30.0,-0.2307])

## Note that 308 is the largest integer to which 10 may be exponentiated and the number be representable as a float
logmax = 308

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
lb = np.array([lbR,lbR,lbR,lbR,lbR,lbR,lbKx,lbc,lbc,lbv,lbv,lbsigma])
ub = np.array([ubR,ubR,ubR,ubR,ubR,ubR,ubKx,ubc,ubc,ubv,ubv,ubsigma])

## Create function for the running of the MCMC
def loglF(Rtot):
    if np.any(np.isinf(Rtot)) or np.any(np.isnan(Rtot)):
        return -float('inf')

    if np.any(np.less(Rtot, lb)) or np.any(np.greater(Rtot, ub)):
        return -float('inf')

    for j in range(9,11):
        if Rtot[j] < 1:
            Rtot[j] = 1
        elif Rtot[j] > 30:
            Rtot[j] = 30
        else:
            Rtot[j] = floor(Rtot[j])

    output = StoneM.NormalErrorCoef(Rtot)

    return(output)

#### Run simulation
niters = 1000

## Set up parameters for parallel-tempered Ensemble Sampler
ndims, nwalkers = int(np.size(lb)), 100
p0 = np.random.uniform(low=0, high=1, size=(nwalkers, ndims))

for ii in range(0, nwalkers):
    p0[ii] = lb + (ub - lb)*p0[ii]

## Set up sampler
sampler = EnsembleSampler(nwalkers,ndims,loglF,2.0,[],{},None,3)

f = h5py.File("mcmc_chain.h5", 'w', libver='latest')
dset = f.create_dataset("data", chunks=True, maxshape=(None, len(lb) + 2), data=np.ndarray((0, len(lb) + 2)))
f.swmr_mode = True
thinTrack = 1
thin = 1

for p, lnprob, lnlike in sampler.sample(p0, iterations=niters, storechain=False):
    if thinTrack < thin:
        thinTrack += 1
    else:
        matOut = np.concatenate((lnprob.reshape(nwalkers, 1), np.arange(0, nwalkers).reshape(nwalkers, 1), p.reshape(nwalkers, ndims)), axis=1)

        fShape = dset.shape
        dset.resize((fShape[0] + np.shape(matOut)[0], fShape[1]))
        dset[fShape[0]:, :] = matOut
        f.flush()

        print(fShape)
        thinTrack = 1
    pass
