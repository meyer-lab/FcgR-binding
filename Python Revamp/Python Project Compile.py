import numpy as np
from math import *
import emcee as mc

##########################################################################################################
## Functions for creation of data for other scripts:

def nchoosek(n,k):
    ## Used in loadData for the matrix biCoefMat
    return factorial(n)/(factorial(k)*factorial(n-k))

def loadData():
    ## This creates the data we will be using in our script
    ##########################################################################################################
    
    ## These are the original MFIs given us by the Nimmerjahn Lab; in iterated list format for eventual conversion
    ## to a NumPy array
    mfi = [[113,5,7,8,38,6,8,10], \
    [441,427,784,172,318,552,900,248], \
    [440,578,997,176,404,392,894,124], \
    [442,407,905,185,322,515,957,242], \
    [388,428,618,139,530,431,810,172], \
    [14,8,9,9,18,9,12,12], \
    [130,177,274,58,266,604,1016,281], \
    [50,23,57,13,149,139,381,48], \
    [184,193,408,87,523,621,1297,281], \
    [44,21,29,17,265,151,343,72], \
    [38,4,4,5,53,5,5,10], \
    [327,308,539,113,660,585,1298,377], \
    [277,203,174,36,533,394,742,156], \
    [307,334,305,135,421,674,1173,405], \
    [148,54,6,20,630,517,1005,145], \
    [7,6,7,4,9,7,9,10], \
    [80,200,262,30,139,737,1108,230], \
    [17,27,40,8,63,111,260,32], \
    [124,231,349,62,442,942,746,244], \
    [33,44,100,21,183,331,605,68], \
    [7,6,8,6,7,7,8,11], \
    [262,676,1015,269,709,1333,1935,698], \
    [14,31,31,14,23,26,68,19], \
    [328,528,790,267,788,1668,2628,891], \
    [9,8,16,10,17,21,46,20], \
    [49,8,14,7,49,8,9,8], \
    [295,596,1016,334,488,813,1330,383], \
    [105,186,293,65,177,362,573,114], \
    [np.nan,623,1055,365,924,1317,1861,676], \
    [122,136,262,91,313,558,1026,239]]

    ## mfiAdj is the background-MFI-adjusted MFI values given above
    mfiAdj = []
    noise = []
    for j in range(len(mfi)):
        if j%5 != 0:
            mfiAdj.append(mfi[j])
        else:
            for k in range(4):
                noise.append(mfi[j])
    mfiAdj = np.array(mfiAdj)-np.array(noise)

    ## mfiAdjMean is the mean-adjusted version of mfiAdj
    temp = np.transpose(mfiAdj)
    means = [np.nanmean(np.concatenate((temp[j],temp[j+4]))) for j in range(4)]
    means2 = np.concatenate((means,means))
    temp = means2
    for j in range(23):
        temp = np.concatenate((temp,means2))
    noise = np.reshape(temp,(24,8))
    mfiAdjMean = mfiAdj/noise

    ######################
    
    ## The NumPy array tnpbsa contains the concentrations of TNP-4-BSA and TNP-26-BSA used in Lux's assays
    tnpbsa4 = 1/67122*1e-3*5
    tnpbsa26 = 1/70928*1e-3*5
    tnpbsa = np.array([tnpbsa4,tnpbsa26])

    ######################

    ## kaBruhns is the matrix of Ka values from Bruhns
    ## For accuracy, the Python implementation of this code will use
    ## Ka values as opposed to Kd, as these were the values which Bruhns
    ## gives in his experiments.
    kaBruhns = [[6.50e7,np.nan,6.10e7,3.40e7], \
    [4.00e6,8.00e4,1.00e6,2.00e5], \
    [4.00e6,4.50e5,1.00e6,2.00e5], \
    [2.00e5,2.50e4,1.70e5,2.00e5], \
    [1.50e6,2.50e4,5.00e6,2.00e5], \
    [1.50e6,8.00e4,5.00e6,2.00e5]]

    kaBruhns = np.array(kaBruhns)

    ######################

    ## meanPerCond is a matrix which contains the mean value for each condition
    ## (after mean adjustment) of the size 24x2
    meanPerCond = []
    for j in range(24):
        temp = []
        for k in range(2):
            temp2 = []
            for l in range(4):
                temp2.append(mfiAdjMean[j,k*4+l])
            temp.append(np.nanmean(np.array(temp2)))
        meanPerCond.append(temp)
    meanPerCond = np.array(meanPerCond)

    ######################
    ## biCoefMat is a matrix such that the nth row has all the integers of the nth row of Pascal's
    ## triangle in order, save the first integer, which is always 1. Used so that nchoosek need not
    ## be called repeatedly in the script.
    biCoefMat = []
    for j in range(30):
        temp = []
        for k in range(j+1):
            temp.append(nchoosek(j+1,k+1))
        while len(temp) < 30:
            temp.append(0)
        biCoefMat.append(temp)
    biCoefMat = np.array(biCoefMat)

    ## ***********************************
    ## This script returns a dictionary wherein each NumPy array can be called with a key of the same
    ## name.
    return {'mfiAdjMean':mfiAdjMean, 'tnpbsa':tnpbsa, 'kaBruhns':kaBruhns, \
            'meanPerCond':meanPerCond, 'biCoefMat':biCoefMat}

##########################################################################################################

def ReqFuncSolver(R, kai, Li, vi, kx):
    ## The purpose of this function is to solver for Req in equation 2 in Stone 2001. This function,
    ## a bisection solver, is necessary for that there does not exist an algebraic solution for Req
    ## in equation 2 from Stone.

    ######################
    ## Convert Ka to Kd for ease of writing this function, and for similarity with original MATLAB function
    kdi = 1/kai
    ## viLikdi is a constant used frequently in this bisection algorithm; to save runtime, it is calculated
    ## once here.
    viLikdi = vi*Li/kdi

    ## a is the lower bound of the bisection;
    ## b is the upper bound of the bisection.
    a = -20
    b = log10(R)
    print(a)
    print(b)
    print(' ')

    ## This algorithm works by generating a value c between a and b at each step and finding whether the solution
    ## is above or below c. After determining which, a new a and b are generated using the pre-existing a, b, and c,
    ## and the algorithm continues. bVal the initial value of the function diffFun at x = b, and cVal is the intial
    ## value of the function diffFun at x = a.
    bVal = diffFun(b,R,vi,kx,viLikdi)
    cVal = diffFun(a,R,vi,kx,viLikdi)
    print(bVal)
    print(cVal)

    ## Is there no root within the interval?
    if bVal*cVal > 0:
        c = 1000
        return c
    
    ## In the case that (b - a > 1e-4 and abs(cVal) > 1e-4) == 1 to begin with.
    c = 1000
    ## Commence algorithm; please see description of algortith above. Note that this bisection algorithm is being used
    ## to find the common logarithm of Req and not Req directly.
    while ((b - a > 1e-4) and (abs(cVal) > 1e-4)):
        c = (a+b)/2
##        print(str(bVal)+'     '+str(cVal))
        cVal = diffFun(c, R, vi, kx, viLikdi)
        
        if cVal*bVal >= 0:
            b = c
            bVal = cVal
        else:
            a = c
    return c

    ######################

def diffFun(x, R, vi, kx, viLikdi):
    ## The function by which the bisection algorithm gauges convergence. The closer the value of diffFun to 0, the closer
    ## x is to the common logarithm of Req.
    x = 10**x
    diff = R-x*(1+viLikdi*(1+kx*x)**(vi-1))
    return diff

########################################################################################################################

def StoneMod(logR,Ka,v,logKx,L0,biCoefMat):
    ## Returns the number of mutlivalent ligand bound to a cell with 10^logR
    ## receptors, granted each epitope of the ligand binds to the receptor
    ## kind in question with dissociation constant Kd and cross-links with
    ## other receptors with crosslinking constant Kx = 10^logKx. All
    ## equations derived from Stone et al. (2001).
    
    ####################################################################################
    ## Convert Ka to Kd for similarity to original MATLAB script. Create Kx from logKx and R from logR
    Kd = 1/Ka
    Kx = 10**logKx
    R = 10**logR
    
    ## Vector of binomial coefficients from biCoefMat; to avoid computation of n choose k in equation 1 from Stone 2001
    biCoefVec = biCoefMat[v-1][0:v]
    Req = 10**ReqFuncSolver(R,Kd,L0,v,Kx)
    
    ## Calculate L, according to equations 1 and 7
    L = 0
    for j in range(v):
        L = L+biCoefVec[j]*Kx**j*Req**(j+1)

    ##************************************************************************************************************
    ## Return the sum of all values L from equation 1 which are pertinent according to equation 7
    return L*L0/Kd

####################################################################################################################

def NormalErrorCoef(Rtot,KaMat,mfiAdjMean,tnpbsa,meanPerCond,biCoefMat):
    ## We are determining the fit of a model using the adjusted Akaike information criterion. Instead of fitting a standard
    ## deviation for each combination of receptor, IgG, and TNP-BSA, we fit a single coefficient sigCoef which, when multiplied
    ## my the mean mean-and-background-adjusted MFI from the matrix meanPerCond, should approximate the standard deviation of
    ## the data.
    sigCoef = 10**Rtot[11]

    ## Also, we fit a coefficient logKxcoef instead of Kx, under suspicion that Kx is proportional to Ka for each combination of
    ## receptor and IgG
    logKxcoef = Rtot[6]

    #######################################
    ## We create a 24x8 matrix called logSqrErrMat, which gives the natural logarithm of the likelihood of our model from
    ## the corresponding data point in mfiAdjMean. Due to the difficulties of NumPy, we do this by creating two 24x4 matrices
    ## and then concatenating them, the left matrix (logSqrErrMatPre0) and the right matrix (logSqrErrMatPre1) corresponding to
    ## the data from TNP-4-BSA and TNP-26-BSA, respectively.
    logSqrErrMatPre0 = []
    logSqrErrMatPre1 = []

    ## Iterate over the two kinds of TNP-BSA
    for j in range(2):
        v = Rtot[9+j]
        c = 10**Rtot[7+j]
        L0 = tnpbsa[j]
        ## Iterate over the six flavors of FcgammaR
        for k in range(6):
            logR = Rtot[k]
            ## Iterate over the four flavors of IgG
            for l in range(4):
                Ka = KaMat[k][l]
                ## Calculate logKx
                Kx = 10**logKxcoef/Ka
                logKx = log10(Kx)
                ## Find the MFI value given by our model
                MFI = c*StoneMod(logR,Ka,v,logKx,L0,biCoefMat)
                ## Find the difference in the projected MFI and the reported MFI for each of the four reported MFIs per condition
                temp = np.array([0]*4)
                for m in range(4):
                    temp[m] = mfiAdjMean[4*k+l][4*j+m]
                mean = meanPerCond[4*k+l][j]
                tempm = []
                for m in range(4):
                    tempm.append(pseudoNormlike(temp[m],MFI,(sigCoef*mean)))
                ## Create each of the 24x4 matrices by concatenation
                tempm = np.array(tempm)
                if j == 0:
                    logSqrErrMatPre0 = np.concatenate((logSqrErrMatPre0,tempm))
                else:
                    logSqrErrMatPre1 = np.concatenate((logSqrErrMatPre1,tempm))

    #################################
    ## Add up and return the log likelihoods from each point in logSwrErrMat
    logSqrErr = 0
    for elem in logSqrErrMat:
        logSqrErr = logSqrErr+np.nansum(elem)
    return logSqrErr

##############################################################################################################################

def pseudoNormlike(x,mu,sigma):
    ## Given a normal distribution of mean mu and standard deviation sigma, this function returns the natural logarithm of the
    ## probability density associated with the point x. Used to compute likelihoods in our calculation of the Akaike information
    ## criterion for a model.
    z = (x - mu) / sigma
    logprob = -0.5*z**2-log(sqrt(2*pi)*sigma)
    return logprob

###############################################################################################################################
###############################################################################################################################
## Run MCMC:


########################################################################################################################################################
########################################################################################################################################################
## Test lines:
print(NormalErrorCoef([1]*12,data['kaBruhns'],data['mfiAdjMean'],data['tnpbsa'],data['meanPerCond'],data['biCoefMat']))

##print(ReqFuncSolver(1000,data['kaBruhns'][0,0],data['tnpbsa'][0],26,1e-10))
