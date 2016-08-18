import matlab.engine
from emcee import *
import numpy
import csv
import time
from multiprocessing import Pool

## For running in parallel
#### Set to 8 if running on VM
#### Set to 5 if running on Ryan's laptop
##p = Pool(8)

## Clear csvs to be used
fd = open('pos.csv','w')
fd.write('')
fd.close()

fd = open('prob.csv','w')
fd.write('')
fd.close()

## Upper and lower bounds of the 12 parameters
lbR = 0
ubR = 8
lbKx = -20
ubKx = 0
lbc = -20
ubc = 5
lbv = 1
ubv = 30
lbsigma = -20
ubsigma = 2

#### Run simulation
nsamples = int(input('Do you want to run the MCMC? If so, list how many \n' \
                 + 'samples.\n'))
## Start MATLAB engine
## (It takes quite a while for the engine to be initialized)
eng = matlab.engine.start_matlab()
## Load necessary parameters for MATLAB functions
eng.NormalErrorCnct()

## Set up parameters for parallel-tempered Ensemble Sampler
nwalkers = 100
ndims = 12

plength = nwalkers*ndims
lnlength = nwalkers

def logl(inp):
    ## Data is input as a Numpy array; must convert to list in order
    ## to input into MATLAB engine

    Rtot = [];
    for rtot in inp:
        Rtot.append(rtot)
    Rtot = matlab.double(Rtot)
    logprob = eng.NormalErrorCnct(Rtot)
    return logprob

sampler = EnsembleSampler(nwalkers,ndims,logl,2.0,[],{},None,1,None,False,None)

## Burn-in run
p0 = numpy.random.rand(ndims*nwalkers).reshape((nwalkers,ndims))
newp0 = []
for walker in p0:
    newwalker = []
    for j in range(ndims):
        if j < 6:
            lb = lbR
            ub = ubR
        elif j == 6:
            lb = lbKx
            ub = ubKx
        elif j < 9:
            lb = lbc
            ub = ubc
        elif j < 11:
            lb = lbv
            ub = ubv
        else:
            lb = lbsigma
            ub = ubsigma
        newwalker.append(walker[j]*(ub-lb)+lb)
    newp0.append(newwalker)
p0 = numpy.array(newp0)
pos, prob, _ = sampler.run_mcmc(p0, 100)
sampler.reset()

## Start timer
start = time.time()

fdpos = open('pos.csv','a')
fdprob = open('prob.csv','a')

## Run sampler for nsamples many counts
for j in range(nsamples):
    pos, prob, _ = sampler.run_mcmc(p0,1)

    posnew = pos.reshape(plength)
    probnew = prob.reshape(lnlength)

    posstore = ''
    probstore = ''
    
    for elem in posnew:
        posstore = posstore+','+str(elem)
    for elem in probnew:
        probstore = probstore+','+str(elem)
        
    posstore = posstore+'\n'
    probstore = probstore+'\n'

    fdpos.write(posstore)
    fdprob.write(probstore)
    
    sampler.reset()
fdpos.close()
fdprob.close()

## End timer
end = time.time()
print('Finished. Time elapsed: '+str(end-start)+' seconds')
