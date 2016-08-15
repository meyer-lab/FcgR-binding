import matlab.engine
from emcee import *
import numpy
import csv
import time

## Clear as csvs to be used, if necessary
query = input('Clean all csvs? If so, say "pls".\n')
if query == 'pls':
    fd = open('p.csv','w')
    fd.write('')
    fd.close()

    fd = open('lnprob.csv','w')
    fd.write('')
    fd.close()

    fd = open('lnlike.csv','w')
    fd.write('')
    fd.close()

#### Run simulation
nsamples = int(input('Do you want to run the MCMC? If so, list how many \n' \
                 + 'samples.\n'))
## Start MATLAB engine
## (It takes quite a while for the engine to be initialized)
eng = matlab.engine.start_matlab()
## Load necessary parameters for MATLAB functions
eng.NormalErrorCnct()

## Set up parameters for parallel-tempered Ensemble Sampler
ntemps = 10
nwalkers = 26
ndims = 12

plength = ntemps*nwalkers*ndims
lnlength = ntemps*nwalkers

def logl(inp):
    ## Data is input as a Numpy array; must convert to list in order
    ## to input into MATLAB engine

    Rtot = [];
    for rtot in inp:
        Rtot.append(rtot)
    Rtot = matlab.double(Rtot)
    logprob = eng.NormalErrorCnct(Rtot)
    return logprob

def logp(inp):
    return 0.0

sampler = PTSampler(ntemps,nwalkers,ndims,logl,logp)

## Burn-in run
p0 = numpy.random.uniform(-1.0,1.0,(ntemps,nwalkers,ndims))
for p, lnprob, lnlike in sampler.sample(p0,1000):
    pass
sampler.reset()

## Start timer
start = time.time()

fdp = open('p.csv','a')
fdlnprob = open('lnprob.csv','a')
fdlnlike = open('lnlike.csv','a')

## Run sampler for nsamples many counts
for j in range(nsamples):
    for p, lnprob, lnlike in sampler.sample(p,lnprob,
                                            lnlike,
                                            1,
                                            1,
                                            False):
        pnew = p.reshape(plength)
        lnprobnew = lnprob.reshape(lnlength)
        lnlikenew = lnlike.reshape(lnlength)

        pstore = ''
        lnprobstore = ''
        lnlikestore = ''
        for elem in pnew:
            pstore = pstore+','+str(elem)
        for k in range(lnlength):
            lnprobstore = lnprobstore+','+str(lnprobnew[k])
            lnlikestore = lnlikestore+','+str(lnlikenew[k])
        pstore = pstore+'\n'
        lnprobstore = lnprobstore+'\n'
        lnlikestore = lnlikestore+'\n'

        fdp.write(pstore)
        fdlnprob.write(lnprobstore)
        fdlnlike.write(lnlikestore)
        
        sampler.reset()
fdp.close()
fdlnprob.close()
fdlnlike.close()

## End timer
end = time.time()
print('Finished. Time elapsed: '+str(end-start)+' seconds')
