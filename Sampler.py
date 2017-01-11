from emcee import EnsembleSampler
import numpy as np
import StoneModel
import h5py
from scipy.optimize import minimize
from joblib import Parallel, delayed

try:
   import cPickle as pickle
except:
   import pickle

newData = True
bestLL = -np.inf

###########################################################
## Load model
StoneM = StoneModel.StoneModel(newData)
###########################################################

# Dump class to a string to store with MCMC chain
StoneMs = pickle.dumps(StoneM, pickle.HIGHEST_PROTOCOL)

# Bounds list for optimization
boundsOpt = list(zip(StoneM.lb.tolist(),StoneM.ub.tolist()))

#### Run simulation
niters = 100000

## Set up parameters for parallel-tempered Ensemble Sampler
ndims, nwalkers = StoneM.Nparams, 4*StoneM.Nparams
p0 = np.random.uniform(low=0, high=1, size=(nwalkers, ndims))

for ii in range(nwalkers):
    p0[ii] = StoneM.lb + (StoneM.ub - StoneM.lb)*p0[ii]

## Set up sampler
sampler = EnsembleSampler(nwalkers,ndims,StoneM.NormalErrorCoef,2.0,[],{},None,16)

f = h5py.File("mcmc_chain.h5", 'w', libver='latest')
dset = f.create_dataset("data", chunks=True, maxshape=(None, StoneM.Nparams + 2), data=np.ndarray((0, StoneM.Nparams + 2)))
dset.attrs["class"] = np.void(StoneMs)
f.swmr_mode = True
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
    pass
