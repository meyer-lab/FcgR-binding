import os
from memoize import memoize
from scipy.special import binom
from scipy.stats import poisson
from scipy.optimize import newton
import numpy as np

np.seterr(over='raise')


def logpdf_sum(x, loc, scale):
    """
    Normal distribution function. Sums over the likelihoods of points in x
    """
    root2 = np.sqrt(2)
    root2pi = np.sqrt(2 * np.pi)
    prefactor = - x.size * np.log(scale * root2pi)
    summand = -np.square((x - loc) / (root2 * scale))
    return prefactor + np.nansum(summand)


@memoize
def nchoosek(n):
    """ A fast cached version of nchoosek. """
    return binom(n, np.arange(n + 1))


def normalizeData(filepath):
    """ Import Lux et al data and normalize by experiment. """

    # Read in the csv data for the first experiments.
    Luxpre = np.loadtxt(filepath, delimiter=',',
                        skiprows=2, usecols=list(range(2, 10)))

    # Copy the data to a new matrix
    newLux = np.copy(Luxpre)

    # Subtract off the corresponding blank measurement
    for (ii, jj) in np.ndindex(Luxpre.shape):
        newLux[ii, jj] = Luxpre[ii, jj] - Luxpre[ii - (ii % 5), jj]

    # Filter out the blank measurements
    newLux = newLux[np.mod(range(newLux.shape[0]), 5) > 0, :]

    # Normalize by the average intensity of each replicate
    for j in range(4):
        newLux[:, (j, j + 4)] = newLux[:, (j, j + 4)] / np.nanmean(newLux[:, (j, j + 4)])

    return newLux


def ReqFuncSolver(R, ka, Li, vi, kx):
    """
    The purpose of this function is to calculate the value of Req (from Eq 1
    from Stone) given parameters R, kai=Ka,Li=L, vi=v, and kx=Kx. It does this
    by performing the bisction algorithm on Eq 2 from Stone. The bisection
    algorithm is used to find log10(Req) which satisfies Eq 2 from Stone.
    """
    viLika = vi*Li*ka

    func = lambda x: R-x*(1+(viLika*np.power((1+kx*x), vi-3))*(1+kx*x)*(1+kx*x))
    fprime = lambda x: -(kx*vi*x+1)*(viLika*np.power((1+kx*x), vi-3))*(1+kx*x) - 1
    fprime2 = lambda x: -kx*(vi-1)*(viLika*np.power((1+kx*x), vi-3))*(2+kx*vi*x)

    if (func(0) * func(R) > 0):
        return np.nan

    return newton(func=func, fprime=fprime, fprime2=fprime2, maxiter=1000, x0=R/2.0, tol=1.0E-9)


def StoneMod(logR, Ka, v, Kx, L0, fullOutput=True):
    '''
    Returns the number of mutlivalent ligand bound to a cell with 10^logR
    receptors, granted each epitope of the ligand binds to the receptor
    kind in question with dissociation constant Kd and cross-links with
    other receptors with crosslinking constant Kx = 10^logKx. All
    equations derived from Stone et al. (2001). Assumed that ligand is at
    saturating concentration L0 = 7e-8 M, which is as it is (approximately)
    for TNP-4-BSA in Lux et al. (2013).
    '''
    v = np.int_(v)

    # Vector of binomial coefficients
    Req = ReqFuncSolver(10.**logR, Ka, L0, v, Kx)
    if np.isnan(Req):
        return (np.nan, np.nan, np.nan, np.nan)

    # Calculate vieq from equation 1
    vieq = L0*Ka*Req*(nchoosek(v)[1::]) * np.power(Kx*Req, np.arange(v))

    # Calculate L, according to equation 7
    Lbound = np.sum(vieq)

    # If we just need the amount of ligand bound, exit here.
    if fullOutput is False:
        return (Lbound, np.nan, np.nan, np.nan, Req)

    # Calculate Rmulti from equation 5
    Rmulti = np.sum(np.multiply(vieq[1:], np.arange(2, v + 1, dtype=np.float)))

    # Calculate Rbound
    Rbnd = np.sum(np.multiply(vieq, np.arange(1, v + 1, dtype=np.float)))

    # Calculate numXlinks from equation 4
    nXlink = np.sum(np.multiply(vieq[1:], np.arange(1, v, dtype=np.float)))

    return (Lbound, Rbnd, Rmulti, nXlink, Req)


class StoneModel(object):
    # This function returns the log likelihood of a point in an MCMC against the ORIGINAL set of data.
    # This function takes in a NumPy array of shape (12) for x, the array KaMat from loadData, the array mfiAdjMean from loadData, the array
    # tnpbsa from loadData, the array meanPerCond from loadData, and the array biCoefMat from loadData. The first six elements are the common
    # logarithms of the receptor expression levels of FcgRIA, FcgRIIA-Arg, FcgRIIA-His, FcgRIIB, FcgRIIIA-Phe, and FcgRIIIA-Val (respectively),
    # the common logarithm of the Kx coefficient (by which the affinity for any receptor-IgG combo is multiplied in order to return Kx), the common
    # logarithms of the MFI-per-TNP-BSA ratios for TNP-4-BSA and TNP-26-BSA, respectively, the effective avidity of TNP-4-BSA, the effective avidity
    # of TNP-26-BSA, and the coefficient by which the mean MFI for a certain combination of FcgR, IgG, and avidity is multiplied to produce the
    # standard deviation of MFIs for that condition.
    def NormalErrorCoefcalc(self, x, fullOutput=False):
        # Set the standard deviation coefficients
        sigCoef = np.power(10, x[self.sigIDX])
        sigCoef2 = np.power(10, x[self.sig2IDX])

        # Keep track of cumulative error
        logSqrErr = 0

        # Fill in Req values for evalutation
        outputReq = np.full((24, 2), np.nan)

        if fullOutput:
            outputFit = np.full((24, 2), np.nan)
            outputLL = np.full((24, 2), np.nan)
            outputRbnd = np.full((24, 2), np.nan)
            outputRmulti = np.full((24, 2), np.nan)
            outputnXlink = np.full((24, 2), np.nan)
            outputLbnd = np.full((24, 2), np.nan)

        # Iterate over each kind of TNP-BSA (4 or 26)
        for j in range(2):
            # Set the effective avidity for the kind of TNP-BSA in question
            v = np.int_(x[self.uvIDX[j]])
            # Set the MFI-per-TNP-BSA conversion ratio for the kind of TNP-BSA in question
            c = 10**x[self.cIDX[j]]
            # Set the ligand (TNP-BSA) concentration for the kind of TNP-BSA in question
            L0 = self.tnpbsa[j]

            # Prior distribution on the ligand valency
            logSqrErr = logSqrErr + poisson.logpmf(v, mu=(4 + j*22))

            # Iterate over each kind of FcgR
            for k in range(6):
                logR = x[k]

                # If we have the receptor expression also fit that data
                if self.newData:
                    logSqrErr = logSqrErr+logpdf_sum(self.Rquant[k],logR,sigCoef2*logR)

                # Iterate over each kind of IgG
                for l in range(4):
                    # Set the affinity for the binding of the FcgR and IgG in question
                    Ka = self.kaBruhns[k][l]
                    if np.isnan(Ka):
                        continue

                    # Setup the data
                    temp = self.mfiAdjMean[4*k+l][4*j:4*j+4]

                    Kx = np.power(10, x[self.kxIDX]) * Ka

                    # Calculate the MFI which should result from this condition according to the model
                    stoneModOut = StoneMod(logR,Ka,v,Kx,L0, fullOutput=fullOutput)
                    MFI = c * stoneModOut[0]
                    if np.isnan(MFI):
                        return -np.inf

                    # Iterate over each real data point for this combination
                    # of TNP-BSA, FcgR, and IgG in question, calculating
                    # the log-likelihood of the point assuming the
                    # calculated point is true.
                    tempm = logpdf_sum(temp, MFI, sigCoef * MFI)
                    if np.isnan(tempm):
                        return -np.inf

                    # Where we will fill the array
                    xIDX = 4 * k + l

                    # Fill in Req values for evalutation
                    outputReq[xIDX, j] = stoneModOut[4]

                    # If the fit was requested output the model predictions
                    if fullOutput:
                        outputFit[xIDX, j] = MFI
                        outputLL[xIDX, j] = tempm
                        outputRbnd[xIDX,j] = stoneModOut[1]
                        outputRmulti[xIDX,j] = stoneModOut[2]
                        outputnXlink[xIDX,j] = stoneModOut[3]
                        outputLbnd[xIDX,j] = stoneModOut[0]

                    # For each TNP-BSA, have an array which includes the
                    # log-likelihoods of all real points in comparison to
                    # the calculated values. Calculate the log-likelihood
                    # of the entire set of parameters by summing all the
                    # calculated log-likelihoods.
                    logSqrErr = logSqrErr + tempm

        if fullOutput:
            return (logSqrErr, outputFit, outputLL, outputRbnd,
                    outputRmulti, outputnXlink, outputLbnd, outputReq)

        return logSqrErr

    def NormalErrorCoef(self, x, fullOutput=False):
        # Return -inf for parameters out of bounds
        if not np.all(np.isfinite(x)):
            return -np.inf

        # Set avidities to integers
        x[self.uvIDX] = np.floor(x[self.uvIDX])

        return self.NormalErrorCoefcalc(x, fullOutput)

    def __init__(self, newData=True):
        ## Find path for csv files, on any machine wherein the repository recepnum1 exists.
        path = os.path.dirname(os.path.abspath(__file__))
        self.TNPs = ['TNP-4', 'TNP-26']
        self.Igs = ['IgG1', 'IgG2', 'IgG3', 'IgG4']
        self.FcgRs = ['FcgRI', 'FcgRIIA-Arg', 'FcgRIIA-His', 'FcgRIIB', 'FcgRIIIA-Phe', 'FcgRIIIA-Val']
        self.pNames = ['Kx1', 'sigConv1', 'sigConv2', 'gnu1', 'gnu2', 'sigma']

        self.newData = newData

        for i in range(6):
            self.pNames.insert(0, 'Rexp')

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

        ## Create vectors for upper and lower bounds
        ## Only allow sampling of TNP-4 up to double its expected avidity.
        ## Lower and upper bounds for avidity are specified here
        self.start = np.array([6., 6., 6., 6., 6., 6., -12.2, -5.6, -5.6, 4, 26, -0.4], dtype=np.float64)

        # Indices for the various elements. Remember that for the new data the receptor
        # expression is concatted
        self.uvIDX = [9, 10]
        self.kxIDX = 6
        self.cIDX = [7, 8]
        self.sigIDX = 11

        if newData:
            ## Create the NumPy array Rquant, where each row represents a particular
            ## IgG (1,2,3, or 4) and each column corresponds to a particular FcgR
            ## (FcgRIA, FcgRIIA-H,FcgRIIA-R, FcgRIIB, FcgRIIIA-F, and FcgRIIIA-V)

            ## Read in the receptor quantifications for the Nimmerjahn Lab's second
            ## set of data. Using the function reader from the csv library, this data
            ## is used to make the iterable object quant, each iterable element of
            ## which is a single-element list containing a string corresponding to
            ## a row in the original csv.
            self.Rquant = np.loadtxt(os.path.join(path,'./data/lux/FcgRquant.csv'), delimiter=',', skiprows=1)
            self.Rquant = np.log10(self.Rquant).transpose().tolist()

            # Remove nan entries from each array
            for i in range(6):
                self.Rquant[i] = np.delete(self.Rquant[i], np.where(np.isnan(self.Rquant[i])))

            # Load and normalize dataset two
            self.mfiAdjMean = normalizeData(os.path.join(path,'./data/lux/New-Fig2B.csv'))

            # We only include a second sigma if new data
            self.sig2IDX = 12
            self.start = np.insert(self.start, self.sig2IDX, -1.2)
            self.pNames.insert(self.sig2IDX, 'sigma2')
        else:
            # Load and normalize dataset one
            self.mfiAdjMean = normalizeData(os.path.join(path,'./data/lux/Luxetal2013-Fig2B.csv'))

        self.Nparams = len(self.start)
