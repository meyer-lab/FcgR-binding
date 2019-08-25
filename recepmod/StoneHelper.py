"""
This function has a number of methods for combining data about predictions
and processing predictions from the StoneMod classes.
"""

import numpy as np
import pandas as pd


def read_chain(filename=None, ffilter=True):
    """ Reads in hdf5 file and returns the instance of StoneModel and MCMC chain """
    import os
    import h5py
    import pickle

    if filename is None:
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./data/test_chain.h5")

    # Open hdf5 file
    f = h5py.File(filename, 'r')

    # Create pointer to main data set
    dset = f['/data']

    if dset is None:
        raise AssertionError("Dataset from hdf5 was read as empty.")

    # Read in StoneModel and unpickle
    StoneMs = dset.attrs['class']
    StoneM = pickle.loads(StoneMs.tobytes())

    cNames = StoneM.pNames
    cNames.insert(0, 'walker')
    cNames.insert(0, 'LL')

    # Read in dataset to Pandas frame
    # Optionally use burn in
    if ffilter is True:
        pdset = pd.DataFrame(dset[13000:, :], columns=cNames)
    else:
        pdset = pd.DataFrame(dset, columns=cNames)

    f.close()

    pdset['gnu1'] = np.floor(pdset['gnu1'])
    pdset['gnu2'] = np.floor(pdset['gnu2'])

    return (StoneM, pdset)


def rep(x, N):
    """ Returns a range with repeated elements. """
    return [item for item in x for _ in range(N)]


def getMedianKx():
    """ Read the MCMC chain and find the median Kx. Cached for sanity. """
    return np.power(10, np.median((read_chain()[1])['Kx1']))


def getMeasuredDataFrame(self):
    """
    Return a dataframe with the measured data labeled with the condition variables
    """
    normData = pd.DataFrame(self.mfiAdjMean)
    normData = pd.melt(normData, value_name="Meas")

    normData = (normData.assign(TNP=rep(self.TNPs, 24 * 4))
                .assign(Ig=self.Igs * 12 * 4)
                .drop('variable', axis=1)
                .assign(FcgR=rep(self.FcgRs, 4) * 8)
                .assign(Expression=rep(self.Rquant, 4) * 8)
                .assign(Ka=np.tile(np.reshape(self.kaBruhns, (-1, 1)), (8, 1)))
               )

    return normData


def getFitPrediction(self, x):
    """
    Return a dataframe with the fit data labeled with the condition variables
    """
    _, outputFit, oLL, oRbnd, oRmulti, onXlink, oLbnd, oReq = self.NormalErrorCoef(
        x, fullOutput=True)

    outputFit = np.reshape(np.transpose(outputFit), (-1, 1))

    dd = (pd.DataFrame(data=outputFit, columns=['Fit'])
          .assign(LL=np.reshape(np.transpose(oLL), (-1, 1)))
          .assign(Ig=self.Igs * 12)
          .assign(FcgR=rep(self.FcgRs, 4) * 2)
          .assign(TNP=rep(self.TNPs, 24))
          .assign(Expression=rep(self.Rquant, 4) * 2)
          .assign(Ka=np.tile(np.reshape(self.kaBruhns, (-1, 1)), (2, 1)))
          .assign(RbndPred=np.reshape(np.transpose(oRbnd), (-1, 1)))
          .assign(RmultiPred=np.reshape(np.transpose(oRmulti), (-1, 1)))
          .assign(nXlinkPred=np.reshape(np.transpose(onXlink), (-1, 1)))
          .assign(LbndPred=np.reshape(np.transpose(oLbnd), (-1, 1)))
          .assign(Req=np.reshape(np.transpose(oReq), (-1, 1)))
         )

    return dd


def getFitMeasMerged(M, x):
    """
    Return the fit and measured data merged into a single dataframe
    """
    fit = getFitPrediction(M, x)
    data = getMeasuredDataFrame(M)

    fit = fit.drop('Expression', axis=1)

    allFrame = fit.merge(data, 'outer', on=('FcgR', 'TNP', 'Ig', 'Ka'))

    return allFrame


def getFitMeasMergedSummarized(M, x):
    fitFrame = getFitMeasMerged(M, x)

    fitFrame['Expression_mean'] = fitFrame.Expression.apply(lambda x: np.power(10, np.mean(x)))

    # Massage data frame into mean and sem of measured values
    fitMean = fitFrame.groupby(['Ig', 'TNP', 'FcgR']).mean().reset_index()
    fitSTD = (fitFrame[['Ig', 'TNP', 'FcgR', 'Meas']]
              .groupby(['Ig', 'TNP', 'FcgR'])
              .sem()
              .reset_index())

    # Reunite the mean and sem summarized values
    fitMean = fitMean.merge(fitSTD, how='outer',
                            on=['Ig', 'TNP', 'FcgR'],
                            suffixes=['_mean', '_std'])

    return fitMean


def getFitMeasSummarized(M):
    fitFrame = getMeasuredDataFrame(M)

    fitFrame['Expression_mean'] = fitFrame.Expression.apply(lambda x: np.power(10, np.mean(x)))

    # Massage data frame into mean and sem of measured values
    fitMean = fitFrame.groupby(['Ig', 'TNP', 'FcgR']).mean().reset_index()
    fitSTD = (fitFrame[['Ig', 'TNP', 'FcgR', 'Meas']].groupby(
        ['Ig', 'TNP', 'FcgR']).sem().reset_index())

    # Reunite the mean and sem summarized values
    fitMean = fitMean.merge(fitSTD, how='outer',
                            on=['Ig', 'TNP', 'FcgR'],
                            suffixes=['_mean', '_std'])

    return fitMean


def geweke(chain1, chain2=None):
    """
    Perform the Geweke Diagnostic between two univariate chains. If two chains are input
    instead of one, Student's t-test is performed instead.
    """
    from scipy.stats import ttest_ind

    len0 = chain1.shape[0]
    if chain2 is None:
        chain2 = chain1[int(np.ceil(len0 / 2)):len0]
        chain1 = chain1[0:int(np.ceil(len0 * 0.1))]
    statistic, pvalue = ttest_ind(chain1, chain2)
    return statistic, pvalue


def geweke_chain(dset, cut=0):
    """
    Perform the Geweke Diagnostic on multiple chains of data contained in a Pandas DataFrame "dset" output by read_chain.
    """
    statistics = []
    pvalues = []
    dsett = dset.drop(['LL', 'walker'], 1).values
    for j in range(dsett.shape[1]):
        statistic, pvalue = geweke(dsett[cut:-1, j])
        statistics.append(statistic)
        pvalues.append(pvalue)
    return statistics, pvalues


def geweke_chains(DSET, cut=0):
    # Perform the Geweke Diagnostic on multiple chains (on along two axes)
    # of data contained in a Pandas Dataframe "dset" output by read_chain.
    nwalkers = int(np.max(DSET['walker'])) + 1
    Statistics = []
    Pvalues = []
    DSETT = DSET.T
    DSETT.columns = [item % nwalkers for item in DSETT.columns]
    for j in range(nwalkers):
        statistics, pvalues = geweke_chain(DSETT[j].T, cut)
        Statistics.append(statistics)
        Pvalues.append(pvalues)
    return Statistics, Pvalues
