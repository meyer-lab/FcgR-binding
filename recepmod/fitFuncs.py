import numpy as np


def startH5File(StoneM, filename):
    """ Dump class to a string to store with MCMC chain. """
    import h5py

    try:
        import cPickle as pickle
    except ImportError:
        import pickle

    StoneMs = pickle.dumps(StoneM, pickle.HIGHEST_PROTOCOL)

    f = h5py.File(filename, 'w', libver='latest')
    dset = f.create_dataset("data",
                            chunks=True,
                            maxshape=(None, StoneM.Nparams + 2),
                            data=np.ndarray((0, StoneM.Nparams + 2)),
                            dtype=np.float32,
                            compression="gzip",
                            compression_opts=9)
    dset.attrs["class"] = np.void(StoneMs)

    return (f, dset)


def getUniformStart(StoneM):
    """ Set up parameters for parallel-tempered Ensemble Sampler """
    ndims, nwalkers = StoneM.Nparams, 4 * StoneM.Nparams
    p0 = np.random.uniform(low=0, high=1, size=(nwalkers, ndims))

    for ii in range(nwalkers):
        p0[ii] = StoneM.lb + (StoneM.ub - StoneM.lb) * p0[ii]

    return (p0, ndims, nwalkers)


def runSampler(niters=100000, thin=200, newData=True, filename="./recepmod/data/test_chain.h5", npar=32):
    """ Run the sampling. """
    from emcee import EnsembleSampler
    from .StoneModel import StoneModel
    from tqdm import tqdm

    # Load model
    StoneM = StoneModel(newData)

    # Get uniform distribution of positions for start
    p0, ndims, nwalkers = getUniformStart(StoneM)

    # Set up sampler
    sampler = EnsembleSampler(nwalkers, ndims, StoneM.NormalErrorCoef, threads=npar)

    if filename is not None:
        f, dset = startH5File(StoneM, filename)

    # Setup thinning tracking
    thinTrack = 0

    for p, lnprob, _ in tqdm(sampler.sample(p0, iterations=niters, storechain=False), total=niters):
        if thinTrack < thin:
            thinTrack += 1
        else:
            matOut = np.concatenate((lnprob.reshape(nwalkers, 1),
                                     np.arange(0, nwalkers).reshape(nwalkers, 1),
                                     p.reshape(nwalkers, ndims)), axis=1)

            if filename is not None:
                fShape = dset.shape
                dset.resize((fShape[0] + np.shape(matOut)[0], fShape[1]))
                dset[fShape[0]:, :] = matOut
                f.flush()

            thinTrack = 1
