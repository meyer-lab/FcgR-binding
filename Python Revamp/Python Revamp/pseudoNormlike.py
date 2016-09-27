from math import *

def pseudoNormlike(x,mu,sigma):
    ## To replace normlike in the function PDF; while normlike returns
    ## negated log probabilities, this function returns log probabilities as
    ## they are.
    z = (x - mu) / sigma
    logprob = -0.5*z**2-log(sqrt(2*pi)*sigma)
    return logprob


