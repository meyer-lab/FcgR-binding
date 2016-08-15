import matlab.engine
from emcee import *
import numpy
import csv
import time

## For csv appending
pstr = 'p'
lnprobstr = 'lnprob'
lnlikestr = 'lnlike'
csv = '.csv'

## Clear as csvs to be used, if necessary
query = input('Clean all csvs? If so, say "pls".\n')
if query == 'pls':
    w = 'w'
    for j in range(6):
        num = str(j+1)
        fd = eval('open(pstr+num+csv,w)')
        fd.write('')
        fd.close()

        fd = eval('open(lnprobstr+num+csv,w)')
        fd.write('')
        fd.close()

        fd = eval('open(lnlikestr+num+csv,w)')
        fd.write('')
        fd.close()

#### Run simulation
nsamples = int(input('Do you want to run the MCMC? If so, list how many \n' \
                 + 'samples.\n'))
## Set up parameters for parallel-tempered Ensemble Sampler
ntemps = 10
nwalkers = 26
ndims = 7

plength = ntemps*nwalkers*ndims
lnlength = ntemps*nwalkers

## For csv appending
a = 'a'

def logl(inp):
    ## Data is input as a Numpy array; must convert to list in order
    ## to input into MATLAB engine

    Rtot = [];
    for rtot in inp:
        Rtot.append(rtot)
    Rtot = matlab.double(Rtot)
    logprob = eng.NormalErrorCnct2(Rtot)
    return logprob

def logp(inp):
    return 0.0

## For each FcgR in Lux's Data
for j in range(6):
    ## Open csvs for appending
    a = 'a'
    pnumstr = pstr+str(j+1)
    lnprobnumstr = lnprobstr+str(j+1)
    lnlikenumstr = lnlikestr+str(j+1)

    fdp = eval('open(pnumstr+csv,a)')
    fdlnprob = eval('open(lnprobnumstr+csv,a)')
    fdlnlike = eval('open(lnlikenumstr+csv,a)')
    
    ## Start MATLAB engine
    ## (It takes quite a while for the engine to be initialized)
    eng = matlab.engine.start_matlab()
    ## Load necessary parameters for MATLAB functions
    eng.NormalErrorCnct2(matlab.double([0.0]),matlab.double([float(j+1)]))

    sampler = PTSampler(ntemps,nwalkers,ndims,logl,logp)

    ## Burn-in run
    p0 = numpy.random.uniform(-1.0,1.0,(ntemps,nwalkers,ndims))
    for p, lnprob, lnlike in sampler.sample(p0,1000):
        pass
    sampler.reset()

    ## Start timer
    start = time.time()

    ## Run sampler for nsamples many counts
    for k in range(nsamples):
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
    
    ## Quit MATLAB engine
    eng.quit()

    ## End iteration timer
    end = time.time()
    print('Iteration '+str(j+1)+' finished. Time elapsed: '+str(end-start)+' seconds')
