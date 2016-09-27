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

## For csv appending
posstr = 'pos'
probstr = 'prob'
csv = '.csv'

## Clear csvs to be used
w = 'w'
for j in range(6):
    num = str(j+1)
    fd = eval('open(posstr+num+csv,w)')
    fd.write('')
    fd.close()

    fd = eval('open(probstr+num+csv,w)')
    fd.write('')
    fd.close()

## Upper and lower bounds of the 7 parameters
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

## Create vectors for upper and lower bounds
lb = numpy.array([lbR,lbKx,lbc,lbc,lbv,lbv,lbsigma])
ub = numpy.array([ubR,ubKx,ubc,ubc,ubv,ubv,ubsigma])

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
ndims = 7

plength = nwalkers*ndims
lnlength = nwalkers

## For csv appending
a = 'a'

def logl(inp):
    ## Data is input as a Numpy array; must convert to list in order
    ## to input into MATLAB engine. First, the point is checked to see
    ## if it fits within the prescribed parameter range

    test1 = numpy.less(inp,lb)
    test2 = numpy.greater(inp,ub)
    if numpy.any(test1) or numpy.any(test2):
        return -numpy.inf
    Rtot = [];
    for rtot in inp:
        Rtot.append(rtot)
    Rtot = matlab.double(Rtot)
    logprob = eng.NormalErrorCnct2(Rtot)
    return logprob

## For each FcgR in Lux's Data
for j in range(6):
    ## Open csvs for appending
    posnumstr = posstr+str(j+1)
    probnumstr = probstr+str(j+1)

    fdpos = eval('open(posnumstr+csv,a)')
    fdprob = eval('open(probnumstr+csv,a)')
    
    ## Start MATLAB engine
    ## (It takes quite a while for the engine to be initialized)
    eng = matlab.engine.start_matlab()
    ## Load necessary parameters for MATLAB functions
    eng.NormalErrorCnct2(matlab.double([0.0]),matlab.double([float(j+1)]))

    sampler = EnsembleSampler(nwalkers,ndims,logl,2.0,[],{},None,1,None,False,None)

    ## Burn-in run
    p0 = numpy.random.rand(ndims*nwalkers).reshape((nwalkers,ndims))
    newp0 = []
    for walker in p0:
        newwalker = []
        for k in range(ndims):
            if k < 1:
                lb = lbR
                ub = ubR
            elif k == 1:
                lb = lbKx
                ub = ubKx
            elif k < 4:
                lb = lbc
                ub = ubc
            elif k < 6:
                lb = lbv
                ub = ubv
            else:
                lb = lbsigma
                ub = ubsigma
            newwalker.append(walker[k]*(ub-lb)+lb)
        newp0.append(newwalker)
    p0 = numpy.array(newp0)
    pos, prob, _ = sampler.run_mcmc(p0, 100)
    sampler.reset()

    ## Start timer
    start = time.time()

    ## Run sampler for nsamples many counts
    for k in range(nsamples):
        pos, prob, _ = sampler.run_mcmc(pos,1)
        
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
    
    ## Quit MATLAB engine
    eng.quit()

    ## End iteration timer
    end = time.time()
    print('Iteration '+str(j+1)+' finished. Time elapsed: '+str(end-start)+' seconds')
