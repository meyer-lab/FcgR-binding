import numpy as np


def startH5File(StoneM, filename):
    """ Dump class to a string to store with MCMC chain. """
    import h5py
    from pickle import dumps, HIGHEST_PROTOCOL

    StoneMs = dumps(StoneM, HIGHEST_PROTOCOL)

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
    from scipy.optimize import minimize

    ndims, nwalkers = StoneM.Nparams, 4 * StoneM.Nparams
    p0 = np.random.normal(scale=0.1, size=(nwalkers, ndims))

    start = minimize(lambda x: -StoneM.NormalErrorCoef(x),
                     StoneM.start, method='nelder-mead')

    for ii in range(nwalkers):
        p0[ii] += start.x

    return (p0, ndims, nwalkers)


def runSampler(niters=400000, thin=400, newData=True, filename="./recepmod/data/test_chain.h5", npar=36):
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
    thinTrack = -thin

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
