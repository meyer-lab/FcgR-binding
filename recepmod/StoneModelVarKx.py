import numpy as np
from scipy.optimize import brentq
from scipy.misc import comb
from memoize import memoize
import warnings
import os
import pandas as pd
from .StoneModel import logpdf_sum, nchoosek, normalizeData, ReqFuncSolver, StoneMod

np.seterr(over = 'raise')

## Kx should be zero clearly when Ka is zero, and should approach a constant
## when Ka is infinitely large. Therefore, using functions of the form
## ax/(K + x) make the most sense. To expand upon what's described here,
## one could create a series of those terms, and specify that each subsequent
## term must have a K value greater than the previous.

class StoneModel:
    ## This function returns the log likelihood of a point in an MCMC against the ORIGINAL set of data.
    ## This function takes in a NumPy array of shape (12) for x, the array KaMat from loadData, the array mfiAdjMean from loadData, the array
    ## tnpbsa from loadData, the array meanPerCond from loadData, and the array biCoefMat from loadData. The first six elements are the common
    ## logarithms of the receptor expression levels of FcgRIA, FcgRIIA-Arg, FcgRIIA-His, FcgRIIB, FcgRIIIA-Phe, and FcgRIIIA-Val (respectively),
    ## the common logarithm of the Kx coefficient (by which the affinity for any receptor-IgG combo is multiplied in order to return Kx), the common
    ## logarithms of the MFI-per-TNP-BSA ratios for TNP-4-BSA and TNP-26-BSA, respectively, the effective avidity of TNP-4-BSA, the effective avidity
    ## of TNP-26-BSA, and the coefficient by which the mean MFI for a certain combination of FcgR, IgG, and avidity is multiplied to produce the
    ## standard deviation of MFIs for that condition.
    def NormalErrorCoefcalc(self, x, fullOutput = False):
        ## Set the standard deviation coefficients
        sigCoef = np.power(10, x[self.sigIDX])
        sigCoef2 = np.power(10, x[self.sig2IDX])

        ## Keep track of cumulative error
        logSqrErr = 0

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
                R = np.power(10, logR)

                # If we have the receptor expression also fit that data
                if self.newData:
                    logSqrErr = logSqrErr+logpdf_sum(self.Rquant[k],logR,sigCoef2*logR)

                ## Iterate over each kind of IgG
                for l in range(4):
                    ## Set the affinity for the binding of the FcgR and IgG in question
                    Ka = self.kaBruhns[k][l]
                    if np.isnan(Ka):
                        continue

                    # Setup the data
                    temp = self.mfiAdjMean[4*k+l][4*j:4*j+4]

                    Kx = np.power(10, x[self.kxIDX]) * (Ka / (Ka + np.power(10, x[self.KdxIDX[0]]))) * (R / (R + np.power(10, x[self.KdxIDX[1]])))

                    ## Calculate the MFI which should result from this condition according to the model
                    stoneModOut = StoneMod(logR,Ka,v,Kx,L0)
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
                        stoneRes = StoneMod(logR,Ka,v,Kx,L0, fullOutput = True)
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

        if fullOutput:
            return (logSqrErr, outputFit, outputLL, outputRbnd, outputRmulti, outputnXlink, outputLbnd, outputReq)

        return logSqrErr

    def NormalErrorCoef(self, x, fullOutput = False):
        # Return -inf for parameters out of bounds
        if np.any(np.isinf(x)) or np.any(np.isnan(x)) or np.any(np.less(x, self.lb)) or np.any(np.greater(x, self.ub)):
            return -np.inf

        # Set avidities to integers
        x[self.uvIDX] = np.floor(x[self.uvIDX])

        return self.NormalErrorCoefcalc(x, fullOutput)

    def __init__(self, newData = True):
        ## Find path for csv files, on any machine wherein the repository recepnum1 exists.
        path = os.path.dirname(os.path.abspath(__file__))
        self.TNPs = ['TNP-4', 'TNP-26']
        self.Igs = ['IgG1', 'IgG2', 'IgG3', 'IgG4']
        self.FcgRs = ['FcgRI', 'FcgRIIA-Arg', 'FcgRIIA-His', 'FcgRIIB', 'FcgRIIIA-Phe', 'FcgRIIIA-Val']
        self.pNames = ['Kx1', 'sigConv1', 'sigConv2', 'gnu1', 'gnu2', 'sigma', 'Kdxa', 'KdxR']

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
            self.Rquant = np.loadtxt(os.path.join(path,'./data/FcgRquant.csv'), delimiter=',', skiprows=1)
            self.Rquant = np.log10(self.Rquant).transpose().tolist()

            # Remove nan entries from each array
            for i in range(6):
                self.Rquant[i] = np.delete(self.Rquant[i], np.where(np.isnan(self.Rquant[i])))

            # Load and normalize dataset two
            self.mfiAdjMean = normalizeData(os.path.join(path,'./data/New-Fig2B.csv'))

            # We only include a second sigma if new data
            self.pNames.insert(12, 'sigma2')
        else:
            # Load and normalize dataset one
            self.mfiAdjMean = normalizeData(os.path.join(path,'./data/Luxetal2013-Fig2B.csv'))

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
        self.kaBruhns = np.loadtxt(os.path.join(path,'./data/FcgR-Ka-Bruhns.csv'), delimiter=',')

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
        lbsigma = -4
        ubsigma = 1
        lKdx = -10
        uKdx = 10

        ## Create vectors for upper and lower bounds
        ## Only allow sampling of TNP-4 up to double its expected avidity.
        ## Lower and upper bounds for avidity are specified here
        if newData:
            self.lb = np.array([lbR,lbR,lbR,lbR,lbR,lbR,lbKx,lbc,lbc, 1 , 20,lbsigma,lbsigma,lKdx,lKdx], dtype = np.float64)
            self.ub = np.array([ubR,ubR,ubR,ubR,ubR,ubR,ubKx,ubc,ubc, 8 , 32,ubsigma,ubsigma,uKdx,uKdx], dtype = np.float64)
        else:
            self.lb = np.array([lbR,lbR,lbR,lbR,lbR,lbR,lbKx,lbc,lbc, 1 , 20,lbsigma], dtype = np.float64)
            self.ub = np.array([ubR,ubR,ubR,ubR,ubR,ubR,ubKx,ubc,ubc, 8 , 32,ubsigma], dtype = np.float64)

        # Indices for the various elements. Remember that for the new data the receptor
        # expression is concatted
        self.uvIDX = [9, 10]
        self.kxIDX = [6]
        self.cIDX = [7, 8]
        self.sigIDX = 11
        self.sig2IDX = 12
        self.KdxIDX = [13, 14]

        self.Nparams = len(self.lb)
