import numpy as np
from emcee import PTSampler
import time
import csv

# Time script
start = time.time()

# Create csv to log points
fd = open('testp.csv','w')
fd.write('')
fd.close()

# mu1 = [1, 1], mu2 = [-1, -1]
mu1 = np.ones(2)
mu2 = -np.ones(2)

# Width of 0.1 in each dimension
sigma1inv = np.diag([100.0, 100.0])
sigma2inv = np.diag([100.0, 100.0])

def logl(x):
    dx1 = x - mu1
    dx2 = x - mu2

    return np.logaddexp(-np.dot(dx1, np.dot(sigma1inv, dx1))/2.0,
                        -np.dot(dx2, np.dot(sigma2inv, dx2))/2.0)

# Use a flat prior
def logp(x):
    return 0.0

ntemps = 20
nwalkers = 100
ndim = 2

sampler=PTSampler(ntemps, nwalkers, ndim, logl, logp)

p0 = np.random.uniform(low=-1.0, high=1.0, size=(ntemps, nwalkers, ndim))
for p, lnprob, lnlike in sampler.sample(p0, iterations=1000):
    pass
sampler.reset()

fd = open('testp.csv','a')
for p, lnprob, lnlike in sampler.sample(p, lnprob0=lnprob,
                                           lnlike0=lnlike,
                                           iterations=10000, thin=10):
    pnew = p.reshape(ntemps*nwalkers*ndim)
    pstore = ''
    for elem in pnew:
        pstore = pstore+','+str(elem)
    pstore = pstore+'\n'
    
    fd.write(pstore)
fd.close()

# Display script runtime
end = time.time()
print('Sript ran in '+str(end-start)+' seconds.')
