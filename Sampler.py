from emcee import EnsembleSampler
import numpy as np
from recepmod import StoneModel
from recepmod.fitFuncs import *

newData = True
bestLL = -np.inf

## Load model
StoneM = StoneModel.StoneModel(newData)

#### Run simulation
niters = 100000

# Get uniform distribution of positions for start
p0, ndims, nwalkers = getUniformStart(StoneM)

## Set up sampler
sampler = EnsembleSampler(nwalkers,ndims,StoneM.NormalErrorCoef,2.0,[],{},None,16)

f, dset = startH5File(StoneM, "mcmc_chain.h5")
thinTrack = 0
thin = 200

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

        print((dset.shape, bestLL))
        thinTrack = 1
