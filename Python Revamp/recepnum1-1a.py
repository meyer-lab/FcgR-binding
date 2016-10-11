from math import *
from emcee import EnsembleSampler
import numpy as np
from Python_Project_Compile import *
import csv
import time
import sys

## Define best
best = np.array([5.7204,5.658,5.9681,5.8991,4.8384,6.1420,-6.8541,-5.7668,-5.5631,7.0,30.0,-0.2307])

## Define nan and inf for sake of ease for rest of script
nan = float('nan')
inf = float('inf')

## Define the maximum and minimum of floats in Python
realmax = sys.float_info.max
realmin = sys.float_info.min
## Note that 308 is the largest integer to which 10 may be exponentiated and the number be representable as a float
logmax = 308

###########################################################
## Load all data from loadData
data = loadData()

mfiAdjMean = data['mfiAdjMean']
tnpbsa = data['tnpbsa']
kaBruhns = data['kaBruhns']
meanPerCond = data['meanPerCond']
biCoefMat = data['biCoefMat']
###########################################################

## Clear csvs to be used
fd = open('pos-1a.csv','w')
fd.write('')
fd.close()

fd = open('prob-1a.csv','w')
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

## Create vectors for upper and lower bounds
lb = np.array([lbR,lbR,lbR,lbR,lbR,lbR,lbKx,lbc,lbc,lbv,lbv,lbsigma])
ub = np.array([ubR,ubR,ubR,ubR,ubR,ubR,ubKx,ubc,ubc,ubv,ubv,ubsigma])

## Create function for the running of the MCMC
def logl(Rtot):
    for j in range(12):
        elem = Rtot[j]
        if (elem == float('inf') or elem == -float('inf') or elem == float('nan')):
            return -inf
    for j in range(9,11):
        if Rtot[j] < 1:
            Rtot[j] = 1
        elif Rtot[j] > 30:
            Rtot[j] = 30
        else:
            Rtot[j] = floor(Rtot[j])

    return NormalErrorCoef(Rtot,kaBruhns,mfiAdjMean,tnpbsa,meanPerCond,biCoefMat)

#### Run simulation
nsamples = int(input('Do you want to run the MCMC? If so, list how many \n' \
                 + 'samples.\n'))

## Set up parameters for parallel-tempered Ensemble Sampler
nwalkers = 100
ndims = 12

plength = nwalkers*ndims
lnlength = nwalkers

## Set up sampler
sampler = EnsembleSampler(nwalkers,ndims,logl,2.0,[],{},None,1,None,False,None)

## Burn-in run
##p0 = np.random.rand(ndims*nwalkers).reshape((nwalkers,ndims))
##newp0 = []
##for walker in p0:
##    newwalker = []
##    for j in range(ndims):
##        if j < 6:
##            lb = lbR
##            ub = ubR
##        elif j == 6:
##            lb = lbKx
##            ub = ubKx
##        elif j < 9:
##            lb = lbc
##            ub = ubc
##        elif j < 11:
##            lb = lbv
##            ub = ubv
##        else:
##            lb = lbsigma
##            ub = ubsigma
##        newwalker.append(walker[j]*(ub-lb)+lb)
##    newp0.append(newwalker)
##p0 = np.array(newp0)
##pos, prob, _ = sampler.run_mcmc(p0, 100)
##sampler.reset()
p0 = best

## Start timer
start = time.time()

fdpos = open('pos-1a.csv','a')
fdprob = open('prob-1a.csv','a')

## Run sampler for nsamples many counts
for j in range(nsamples):
    pos, prob, _ = sampler.run_mcmc(p0,1)
    print(pos)

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
