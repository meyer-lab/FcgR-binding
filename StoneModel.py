import numpy as np
from scipy.optimize import brentq
from scipy.misc import comb
from memoize import memoize
import warnings
from os.path import join
import pandas as pd

np.seterr(over = 'raise')

# Calculates the standard error (without adjustment or weight) of a set of data
# in a 1D numpy array, ignoring all NaNs
def nansem(x):
    std = np.nanstd(x,axis=0)
    temp = []
    for j in range(x.shape[1]):
        count = 0
        for elem in x[:,j]:
            if not np.isnan(elem):
                count += 1
        temp.append(count)
    return std/np.sqrt(np.fromiter(temp,np.float))
        
# Normal distribution function. Sums over the likelihoods of points in x
def logpdf_sum(x, loc, scale):
    root2 = np.sqrt(2)
    root2pi = np.sqrt(2*np.pi)
    prefactor = - x.size * np.log(scale * root2pi)
    summand = -np.square((x - loc)/(root2 * scale))
    return  prefactor + np.nansum(summand)

# A fast cached version of nchoosek
@memoize
def nchoosek(n, k):
    return comb(n, k, exact=True)

# Normalize the input data taking into account batch effects
def normalizeData(filepath):
    ## To begin, read in the MFI measurements from both of Lux's experiments from
    ## their respective csvs. Then, subtract background MFIs from these nominal
    ## MFIs. Then, normalize the data by replicate. For each step after the
    ##reading, I manipulated the csv data in different ways, which are explained
    ## in the comments. Please refer to these comments to understand what is
    ## going on, especially with variables of the name "temp$." All
    ## variables with such names are only meant to construct mfiAdjMean1 (from
    ## Lux's first experiments) and mfiAdjMean2 (from Lux's second experiments).

    ## Read in the csv data for the first experiments.
    Luxpre = np.loadtxt(filepath, delimiter=',', skiprows=2, usecols=list(range(2,10)))

    ## The first row in every set of five rows in Luxpre consists of background
    ## MFIs. Lux is made by taking each of the four non-background MFIs from
    ## reach cluster of 5 from Luxpre, subtracting the corresponding background
    ## MFI from each, and then forming a NumPy array of shape (24,8) from all of
    ## these collectively. The final result, Lux, will be a NumPy array of
    ## shape (1,192).
    Lux = np.array([])
    for j in range(len(Luxpre)):
        if j%5 == 0:
            temp = np.array(Luxpre[j])
        else:
            temp2 = np.array(Luxpre[j])-temp
            Lux = np.concatenate((Lux,temp2),0)
    ## Reshape book5 into a NumPy array of shape (24,8), the actual shape of the
    ## MFIs from Lux's original experiments.
    Lux = np.reshape(Lux,(24,8))

    # Normalize by the average intensity of each replicate
    for j in range(4):
        Lux[:,(j,j+4)] = Lux[:,(j,j+4)] / np.nanmean(np.nanmean(Lux[:,(j,j+4)]))

    return(Lux)

## The purpose of this function is to calculate the value of Req (from Equation 1 from Stone) given parameters R,
## kai=Ka,Li=L, vi=v, and kx=Kx. It does this by performing the bisction algorithm on Equation 2 from Stone. The
## bisection algorithm is used to find the value of log10(Req) which satisfies Equation 2 from Stone.
def ReqFuncSolver(R, ka, Li, vi, kx):
    ## a is the lower bound for log10(Req) bisecion. By Equation 2, log10(Req) is necessarily lower than log10(R).
    a = -40
    b = np.log10(R)

    ## Create anonymous function diffFunAnon which calls diffFun for parameters R, vi=v, kx=Kx, and viLikdi.
    ## This function subtracts the right side of Equation 2 from Stone from the left side of the same Equation. The
    ## bisection algorithm is run using this function so as to calculate log10(Req) which satisfies all parameters.
    ## Each time this function is called: x is log10 of the value of Req being tested, R is R from Stone 2, vi is v from
    ## Stone 2, kx is Kx from Stone 2, and viLikdi is a product which is constant over all iterations of the bisection
    ## algorithm over diffFun for a single calling of ReqFuncSolver.
    diffFunAnon = lambda x: R-(10**x)*(1+vi*Li*ka*(1+kx*(10**x))**(vi-1))

    try:
        if diffFunAnon(a)*diffFunAnon(b) > 0:
            return np.nan
    except FloatingPointError:
        return np.nan

    ## Implement the bisection algorithm using SciPy's brentq. Please see SciPy documentation for rationale behind
    ## input parameter not described beforehand. Brentq is ~2x faster than bisect
    logReq = brentq(diffFunAnon, a, b, disp=False)

    return logReq

class StoneModel:
    def StoneMod(self,logR,Ka,v,Kx,L0,fullOutput = False):
        ## Returns the number of mutlivalent ligand bound to a cell with 10^logR
        ## receptors, granted each epitope of the ligand binds to the receptor
        ## kind in question with dissociation constant Kd and cross-links with
        ## other receptors with crosslinking constant Kx = 10^logKx. All
        ## equations derived from Stone et al. (2001). Assumed that ligand is at
        ## saturating concentration L0 = 7e-8 M, which is as it is (approximately)
        ## for TNP-4-BSA in Lux et al. (2013).
        v = np.int_(v)

        ## Vector of binomial coefficients
        Req = 10**ReqFuncSolver(10**logR,Ka,L0,v,Kx)
        if np.isnan(Req):
            return (np.nan, np.nan, np.nan, np.nan)

        # Calculate vieq from equation 1
        vieqIter = (L0*Ka*nchoosek(v,j+1)*Kx**j*Req**(j+1) for j in range(v))
        vieq = np.fromiter(vieqIter, np.float, count = v)

        ## Calculate L, according to equation 7
        Lbound = np.sum(vieq)

        # If we just need the amount of ligand bound, exit here.
        if fullOutput == False:
            return (Lbound, np.nan, np.nan, np.nan, Req)

        # Calculate Rmulti from equation 5
        RmultiIter = ((j+1)*vieq[j] for j in range(1,v))
        Rmulti = np.sum(np.fromiter(RmultiIter, np.float, count = v-1))

        # Calculate Rbound
        RbndIter = ((j+1)*vieq[j] for j in range(v))
        Rbnd = np.sum(np.fromiter(RbndIter, np.float, count = v))

        # Calculate numXlinks from equation 4
        nXlinkIter = (j*vieq[j] for j in range(1,v))
        nXlink = np.sum(np.fromiter(nXlinkIter, np.float, count = v-1))

        return (Lbound, Rbnd, Rmulti, nXlink, Req)

    ## This function returns the log likelihood of a point in an MCMC against the ORIGINAL set of data.
    ## This function takes in a NumPy array of shape (12) for x, the array KaMat from loadData, the array mfiAdjMean from loadData, the array
    ## tnpbsa from loadData, the array meanPerCond from loadData, and the array biCoefMat from loadData. The first six elements are the common
    ## logarithms of the receptor expression levels of FcgRIA, FcgRIIA-Arg, FcgRIIA-His, FcgRIIB, FcgRIIIA-Phe, and FcgRIIIA-Val (respectively),
    ## the common logarithm of the Kx coefficient (by which the affinity for any receptor-IgG combo is multiplied in order to return Kx), the common
    ## logarithms of the MFI-per-TNP-BSA ratios for TNP-4-BSA and TNP-26-BSA, respectively, the effective avidity of TNP-4-BSA, the effective avidity
    ## of TNP-26-BSA, and the coefficient by which the mean MFI for a certain combination of FcgR, IgG, and avidity is multiplied to produce the
    ## standard deviation of MFIs for that condition.
    def NormalErrorCoefcalc(self, x, fullOutput = False):
        ## Set the standard deviation coefficient
        sigCoef = np.power(10, x[self.sigIDX])

        ## Keep track of cumulative error
        logSqrErr = 0

        ## Calculate the Kx value for the combination of FcgR and IgG in question. Then, take the common logarithm of this value.
        Kx = np.power(10, x[self.kxIDX])

        # Fill in Req values for evalutation
        outputReq = np.full((24,2), np.nan)

        if fullOutput:
            outputFit = np.full((24,2), np.nan)
            outputLL = np.full((24,2), np.nan)
            outputRbnd = np.full((24,2), np.nan)
            outputRmulti = np.full((24,2), np.nan)
            outputnXlink = np.full((24,2), np.nan)
            outputLbnd = np.full((24,2), np.nan)

        ## Iterate over each kind of TNP-BSA (4 or 26)
        for j in range(2):
            ## Set the effective avidity for the kind of TNP-BSA in question
            v = x[self.uvIDX[j]]
            ## Set the MFI-per-TNP-BSA conversion ratio for the kind of TNP-BSA in question
            c = 10**x[self.cIDX[j]]
            ## Set the ligand (TNP-BSA) concentration for the kind of TNP-BSA in question
            L0 = self.tnpbsa[j]

            ## Iterate over each kind of FcgR
            for k in range(6):
                logR = x[k]

                # If we have the receptor expression also fit that data
                if self.newData:
                    logSqrErr = logSqrErr+logpdf_sum(logR, self.Rquant[k], self.RquantS[k])

                ## Iterate over each kind of IgG
                for l in range(4):
                    ## Set the affinity for the binding of the FcgR and IgG in question
                    Ka = self.kaBruhns[k][l]
                    if np.isnan(Ka):
                        continue

                    # Setup the data
                    temp = self.mfiAdjMean[4*k+l][4*j:4*j+4]

                    ## Calculate the MFI which should result from this condition according to the model
                    stoneModOut = self.StoneMod(logR,Ka,v,Kx,L0)
                    MFI = c*stoneModOut[0]
                    if np.isnan(MFI):
                        return -np.inf

                    ## Iterate over each real data point for this combination of TNP-BSA, FcgR, and IgG in question, calculating the log-likelihood
                    ## of the point assuming the calculated point is true.
                    tempm = logpdf_sum(temp, MFI, sigCoef*MFI)
                    if np.isnan(tempm):
                        return -np.inf

                    # Fill in Req values for evalutation
                    outputReq[4*k+l,j] = stoneModOut[4]

                    # If the fit was requested output the model predictions
                    if fullOutput:
                        stoneRes = self.StoneMod(logR,Ka,v,Kx,L0, fullOutput = True)
                        outputFit[4*k+l,j] = MFI
                        outputLL[4*k+l, j] = tempm
                        outputRbnd[4*k+l,j] = stoneRes[1]
                        outputRmulti[4*k+l,j] = stoneRes[2]
                        outputnXlink[4*k+l,j] = stoneRes[3]
                        outputLbnd[4*k+l,j] = stoneRes[0]

                    # Skip IIIA-Phe Ig2 and Ig4, because the affinity values seem inconsistent
                    if k == 4 and l % 2 > 0:
                        continue

                    ## For each TNP-BSA, have an array which includes the log-likelihoods of all real points in comparison to the calculated values.
                    ## Calculate the log-likelihood of the entire set of parameters by summing all the calculated log-likelihoods.
                    logSqrErr = logSqrErr+tempm

        corVal = (np.min([np.nanmin(outputReq[:,0] - outputReq[:,1]), 0]))

        if fullOutput:
            return (logSqrErr, outputFit, outputLL, outputRbnd, outputRmulti, outputnXlink, outputLbnd, outputReq)

        return logSqrErr + corVal

    def NormalErrorCoef(self, x, fullOutput = False):
        # Return -inf for parameters out of bounds
        if np.any(np.isinf(x)) or np.any(np.isnan(x)) or np.any(np.less(x, self.lb)) or np.any(np.greater(x, self.ub)):
            return -np.inf

        # Set avidities to integers
        x[self.uvIDX] = np.floor(x[self.uvIDX])

        return self.NormalErrorCoefcalc(x, fullOutput)

    def __init__(self, newData = True):
        ## Find path for csv files, on any machine wherein the repository recepnum1 exists.
        path = './Nimmerjahn Lab and Bruhns Data'
        self.TNPs = ['TNP-4', 'TNP-26']
        self.Igs = ['IgG1', 'IgG2', 'IgG3', 'IgG4']
        self.FcgRs = ['FcgRI', 'FcgRIIA-Arg', 'FcgRIIA-His', 'FcgRIIB', 'FcgRIIIA-Phe', 'FcgRIIIA-Val']
        self.pNames = ['Kx1', 'sigConv1', 'sigConv2', 'gnu1', 'gnu2', 'sigma']

        self.newData = newData

        for i in range(6):
            self.pNames.insert(0, 'Rexp')

        if newData:
            ## Create the NumPy array Rquant, where each row represents a particular
            ## IgG (1,2,3, or 4) and each column corresponds to a particular FcgR
            ## (FcgRIA, FcgRIIA-H,FcgRIIA-R, FcgRIIB, FcgRIIIA-F, and FcgRIIIA-V)

            ## Read in the receptor quantifications for the Nimmerjahn Lab's second
            ## set of data. Using the function reader from the csv library, this data
            ## is used to make the iterable object quant, each iterable element of
            ## which is a single-element list containing a string corresponding to
            ## a row in the original csv.
            self.Rquant = np.loadtxt(join(path,'FcgRquant.csv'), delimiter=',', skiprows=1)

            self.Rquant = np.log10(self.Rquant)

            self.RquantS = nansem(self.Rquant)
            self.Rquant = np.nanmean(self.Rquant, axis=0)

            # Load and normalize dataset two
            self.mfiAdjMean = normalizeData(join(path,'New-Fig2B.csv'))
        else:
            # Load and normalize dataset one
            self.mfiAdjMean = normalizeData(join(path,'Luxetal2013-Fig2B.csv'))

        ## Define the matrix of Ka values from Bruhns
        ## For accuracy, the Python implementation of this code will use
        ## Ka values as opposed to Kd, as these were the values which Bruhns
        ## gives in his experiments. These are read in from a csv in the
        ## folder Nimmerjahn Lab and Bruhns Data. Each row represents a particular
        ## FcgR (FcgRIA, FcgRIIA-H, FcgRIIA-R, FcgRIIB, FcgRIIIA-F, FcgRIIIA-V)
        ## and each column represents a particular IgG(1, 2, 3, 4).

        ## First, read in the csv. It will result in an iterable object, wherein
        ## each element is a single-element list containing a single string, each
        ## string corresponding to a single row from the csv.
        self.kaBruhns = np.loadtxt(join(path,'FcgR-Ka-Bruhns.csv'), delimiter=',')

        ## Define concentrations of TNP-4-BSA and TNP-26-BSA, respectively
        ## These are put into the numpy array "tnpbsa"
        self.tnpbsa = np.array([1/67122,1/70928])*1e-3*5

        # Set upper and lower bounds
        ## Upper and lower bounds of the 12 parameters
        lbR = 3
        ubR = 8
        lbKx = -25
        ubKx = 3
        lbc = -10
        ubc = 5
        lbv = 1
        ubv = 30
        lbsigma = -4
        ubsigma = 1

        ## Create vectors for upper and lower bounds
        ## Only allow sampling of TNP-4 up to double its expected avidity.
        if newData:
            self.lb = np.array([lbR,lbR,lbR,lbR,lbR,lbR,lbKx,lbc,lbc,lbv,lbv,lbsigma], dtype = np.float64)
            self.ub = np.array([ubR,ubR,ubR,ubR,ubR,ubR,ubKx,ubc,ubc,ubv,ubv,ubsigma], dtype = np.float64)
        else:
            self.lb = np.array([lbR,lbR,lbR,lbR,lbR,lbR,lbKx,lbc,lbc,lbv,lbv,lbsigma], dtype = np.float64)
            self.ub = np.array([ubR,ubR,ubR,ubR,ubR,ubR,ubKx,ubc,ubc,ubv,ubv,ubsigma], dtype = np.float64)

        # Indices for the various elements. Remember that for the new data the receptor
        # expression is concatted
        self.uvIDX = [9, 10]
        self.kxIDX = [6]
        self.cIDX = [7, 8]
        self.sigIDX = 11

        self.Nparams = len(self.lb)
