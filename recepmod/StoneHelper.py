## This function has a number of methods for combining data about predictions
## and processing predictions from the StoneMod classes.

import numpy as np
import pandas as pd
import h5py
from tqdm import trange
from scipy.stats import ttest_ind

try:
    import cPickle as pickle
except ImportError:
    import pickle

# Reads in hdf5 file and returns the instance of StoneModel and MCMC chain
def read_chain(filename):
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
    pdset = pd.DataFrame(dset.value, columns = cNames)

    pdset['gnu1'] = np.floor(pdset['gnu1'])
    pdset['gnu2'] = np.floor(pdset['gnu2'])

    f.close()

    return (StoneM, pdset)

def rep(x, N):
    return [item for item in x for i in range(N)]

# Return a dataframe with the measured data labeled with the condition variables
def getMeasuredDataFrame(self):
    normData = pd.DataFrame(self.mfiAdjMean)
    normData = pd.melt(normData, value_name = "Meas")

    normData = (normData.assign(TNP = rep(self.TNPs, 24*4))
                .assign(Ig = self.Igs*12*4)
                .drop('variable', axis = 1)
                .assign(FcgR = rep(self.FcgRs, 4)*8)
                .assign(Expression = rep(self.Rquant, 4)*8)
                .assign(Ka = np.tile(np.reshape(self.kaBruhns, (-1,1)), (8, 1)))
               )

    return normData

# Return a dataframe with the fit data labeled with the condition variables
def getFitPrediction(self, x):
    _, outputFit, outputLL, outputRbnd, outputRmulti, outputnXlink, outputLbnd, outputReq = self.NormalErrorCoef(x, fullOutput = True)

    outputFit = np.reshape(np.transpose(outputFit), (-1, 1))

    dd = (pd.DataFrame(data = outputFit, columns = ['Fit'])
          .assign(LL = np.reshape(np.transpose(outputLL), (-1, 1)))
          .assign(Ig = self.Igs*12)
          .assign(FcgR = rep(self.FcgRs, 4)*2)
          .assign(TNP = rep(self.TNPs, 24))
          .assign(Expression = rep(self.Rquant, 4)*2)
          .assign(Ka = np.tile(np.reshape(self.kaBruhns, (-1,1)), (2, 1)))
          .assign(RbndPred = np.reshape(np.transpose(outputRbnd), (-1, 1)))
          .assign(RmultiPred = np.reshape(np.transpose(outputRmulti), (-1, 1)))
          .assign(nXlinkPred = np.reshape(np.transpose(outputnXlink), (-1, 1)))
          .assign(LbndPred = np.reshape(np.transpose(outputLbnd), (-1, 1)))
          .assign(Req = np.reshape(np.transpose(outputReq), (-1, 1)))
         )

    return dd

def mapMCMC(dFunction, pSet):
    """
    This function takes (1) a function that takes a parameter set and
    returns a dataframe and (2) a list of parameter sets. It returns a dataframe
    with all the individual dataframe outputs stacked, and a number identifier for
    which parameter set each set of quantities came from
    """
    # Set the function to pass back results
    funFunc = lambda ii: dFunction(pSet.iloc[ii,:]).assign(pSetNum = ii)

    # Iterate over each parameter set, output to a list
    retVals = map(funFunc, trange(pSet.shape[0]))

    # Concatenate all the dataframes vertically and return
    return pd.concat(retVals)

# Reduce the collection of predictions to various summary statistics.
def reduceMCMC(frameList, groupByC = ['Ig', 'FcgR', 'TNP'], dropC = ['Expression', 'pSetNum']):
    # Drop indicated columns
    frameList = frameList.drop(dropC, axis = 1).groupby(groupByC)

    # Summarize the collections in various ways
    frameListMean = frameList.mean().reset_index()
    frameListStd = frameList.std().reset_index()
    frameListMedian = frameList.median().reset_index()
    frameListMin = frameList.min().reset_index()
    frameListMax = frameList.max().reset_index()
    frameListLowCI = frameList.quantile(0.025).reset_index()
    frameListHighCI = frameList.quantile(0.975).reset_index()

    # Merge each frame together with a suffix to indicate what each quantity is
    frameAgg = frameListMean.merge(frameListStd, on = groupByC, suffixes = ('_mean', '_std'))
    frameAgg = frameAgg.merge(frameListMedian, on = groupByC, suffixes = ('', '_median'))
    frameAgg = frameAgg.merge(frameListMin, on = groupByC, suffixes = ('', '_min'))
    frameAgg = frameAgg.merge(frameListMax, on = groupByC, suffixes = ('', '_max'))
    frameAgg = frameAgg.merge(frameListLowCI, on = groupByC, suffixes = ('', '_lCI'))
    frameAgg = frameAgg.merge(frameListHighCI, on = groupByC, suffixes = ('', '_uCI'))

    return frameAgg

# Return the fit and measured data merged into a single dataframe
def getFitMeasMerged(self, x):
    fit = getFitPrediction(self, x)
    data = getMeasuredDataFrame(self)

    fit = fit.drop('Expression', axis = 1)

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
    fitMean = fitMean.merge(fitSTD, how = 'outer',
                            on = ['Ig', 'TNP', 'FcgR'],
                            suffixes = ['_mean', '_std'])

    return fitMean

def getFitMeasSummarized(M):
    fitFrame = getMeasuredDataFrame(M)

    fitFrame['Expression_mean'] = fitFrame.Expression.apply(lambda x: np.power(10, np.mean(x)))

    # Massage data frame into mean and sem of measured values
    fitMean = fitFrame.groupby(['Ig', 'TNP', 'FcgR']).mean().reset_index()
    fitSTD = (fitFrame[['Ig', 'TNP', 'FcgR', 'Meas']].groupby(['Ig', 'TNP', 'FcgR']).sem().reset_index())

    # Reunite the mean and sem summarized values
    fitMean = fitMean.merge(fitSTD, how = 'outer',
                            on = ['Ig', 'TNP', 'FcgR'],
                            suffixes = ['_mean', '_std'])

    return fitMean

def mapStore(dset, M):
    frameList = mapMCMC(lambda x: getFitPrediction(M,x),dset.as_matrix()[:,2:])
    frameList.to_pickle('mapped_chain.pkl')

def reduce():
    frameList = pd.read_pickle('mapped_chain.pkl')
    return reduceMCMC(frameList)

def geweke(chain1, chain2=None):
    # Perform the Geweke Diagnostic between two univariate chains. If two chains are input instead of one, Student's t-test is performed instead.
    len0 = chain1.shape[0]
    if not chain2:
        chain2 = chain1[int(np.ceil(len0/2)):len0]
        chain1 = chain1[int(np.ceil(len0*0.1)):int(np.ceil(len0*0.2))]
    statistic, pvalue = ttest_ind(chain1,chain2)
    return statistic, pvalue
            
def geweke_chain(dset):
    # Perform the Geweke Diagnostic on multiple chains of data contained in a Pandas DataFrame "dset" output by read_chain.
    statistics = []
    pvalues = []
    dsett = dset.drop(['LL','walker'],1).as_matrix()
    for j in range(dsett.shape[1]):
        statistic, pvalue = geweke(dsett[:,j])
        statistics.append(statistic)
        pvalues.append(pvalue)
    return statistics, pvalues

def geweke_chains(DSET):
    return 0
