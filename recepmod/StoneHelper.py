import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.colors as mcolors
from matplotlib import rc
from matplotlib.font_manager import FontProperties
import h5py
from tqdm import tqdm
import seaborn as sns
from .StoneModel import StoneModel

try:
   import cPickle as pickle
except:
   import pickle

def seaborn_colorblindGet():
   # This function collects the collor palette settings used in seaborn-colorblind, so as
   # to get all of seaborn's colors without the unwanted formatting effects of seaborn
   # backColor is the background color used in seaborn's colorblind setting
   backColor = (234,234,242)
   backColor = tuple((np.array(backColor)/255).tolist())
   Colors = sns.color_palette('colorblind')
   Colors = sns.color_palette('muted')
   Colors.insert(0,backColor)
   Colors = np.transpose(np.array(Colors))
   Colors = pd.DataFrame(Colors,columns=(['back-color']+['color']*6))
   backColor = (float(Colors[['back-color']].values[j]) for j in range(3))
   colorspre = np.transpose(Colors[['color']].values)
   colors = []
   for j in range(6):
      pre = colorspre[j]
      temp = []
      for k in range(3):
         temp.append(float(pre[k]))
      colors.append(tuple(temp))
   return colors, backColor

colors, backColor = seaborn_colorblindGet()

Igs = {'IgG1':'o', 'IgG2':'d', 'IgG3':'s', 'IgG4':'^'}

fcgrs = ['FcgRI','FcgRIIA-131R','FcgRIIA-131H','FcgRIIB','FcgRIIIA-158F','FcgRIIIA-158V']
FcgRs = {}
for j in range(len(fcgrs)):
    FcgRs[fcgrs[j]] = colors[j]
igs = [elem for elem in Igs]
fcgrs = [elem for elem in FcgRs]

# Reads in hdf5 file and returns the instance of StoneModel and MCMC chain
def read_chain(filename):
    # Open hdf5 file
    f = h5py.File(filename, 'r')

    # Create pointer to main data set
    dset = f['/data']

    if dset == None:
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
    logSqrErr, outputFit, outputLL, outputRbnd, outputRmulti, outputnXlink, outputLbnd, outputReq = self.NormalErrorCoef(x, fullOutput = True)

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

# This function takes (1) a function that takes a parameter set and
# returns a dataframe and (2) a list of parameter sets. It returns a dataframe
# with all the individual dataframe outputs stacked, and a number identifier for
# which parameter set each set of quantities came from
def mapMCMC(dFunction, pSet):
    # Make a list for all the dataframes
    retVals = list()

    # Iterate over each parameter set
    TQDM = tqdm(range(pSet.shape[0]))
    TQDM.mininterval=60;
    TQDM.maxinterval=120;
    for ii in TQDM:
        # Call the passed function and add the output to the list
        retVals.append(dFunction(pSet[ii,:]).assign(pSetNum = ii))

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
    fitSTD = (fitFrame[['Ig', 'TNP', 'FcgR', 'Meas']].groupby(['Ig', 'TNP', 'FcgR']).sem().reset_index())

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

def makeFcIgLegend():
    patches = list()

    for f in FcgRs:
        patches.append(mpatches.Patch(color=FcgRs[f], label=f))

    for j in Igs:
        patches.append(mlines.Line2D([], [], color='black', marker=Igs[j], markersize=7, label=j, linestyle='None'))

    return patches

def plotFit(fitMean,ax=None, backGray=True):
    # This should take a merged and summarized data frame
    fitMeanPre = fitMean[['Fit','Meas_mean','Meas_std']].as_matrix()
    if ax == None:
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(1, 1, 1)

    for j in range(len(Igs)):
        for k in range(len(FcgRs)):
            for l in range(2):
                if l == 0:
                    mfcVal = 'None'
                else:
                    mfcVal = FcgRs[fcgrs[k]]
                ax.errorbar(fitMeanPre[8*j+k+4*l][0],fitMeanPre[8*j+k+4*l][1]+0.01,yerr=fitMeanPre[8*j+k+4*l][2],marker=Igs[igs[j]],mfc=mfcVal,mec=FcgRs[fcgrs[k]],ecolor=FcgRs[fcgrs[k]],linestyle='None')

    ax.legend(handles=makeFcIgLegend(), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot([0.08, 10], [0.08, 10])
    ax.set_ylim(0.01, 10)
    ax.set_xlim(0.08, 70)
    plt.xlabel('Fitted prediction')
    plt.ylabel('Measured ligand binding')
    if backGray:
        ax.set_facecolor(backColor)

def plotQuant(fitMean, nameFieldX, nameFieldY, ax=None, backGray=True, legend=True):
    # This should take a merged and summarized data frame

    if ax == None:
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(1, 1, 1)

    for j in Igs:
        for f in FcgRs:
            for x in range(2):
                temp = fitMean[fitMean['Ig'] == j]
                temp = temp[temp['FcgR'] == f]
                color = FcgRs[f]

                if x == 0:
                    temp = temp[temp['TNP'] == 'TNP-4']
                    mfcVal = 'None'
                else:
                    temp = temp[temp['TNP'] != 'TNP-4']
                    mfcVal = color

                ax.errorbar(temp[nameFieldX], temp[nameFieldY], marker = Igs[j],
                            mfc = mfcVal, mec = color, ecolor = color,
                            linestyle = 'None')

    if legend:
        ax.legend(handles=makeFcIgLegend())

    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.ylabel(nameFieldY)
    plt.xlabel(nameFieldX)
    if backGray:
        ax.set_facecolor(backColor)

def LLscatter(ax=None,backGray=True):
    if ax == None:
        ax = plt.gca()
    dset.plot('LL', 'gnu2', 'scatter',ax=ax)
    if backGray:
        ax.set_facecolor(backColor)
    plt.show()

def gnuScatter(ax=None,backGray=True):
    if ax == None:
        ax = plt.gca()
    dsett.plot(x = 'gnu1', y = 'gnu2', kind = 'scatter', c = 'LL', s = 50,ax=ax)
    plt.xlabel('gnu1')
    if backGray:
        ax.set_facecolor(backColor)
    plt.show()

def mapStore():
   frameList = mapMCMC(lambda x: getFitPrediction(M,x),dset.as_matrix()[:,2:])
   frameList.to_pickle('mapped_chain.pkl')

def reduce():
   frameList = pd.read_pickle('mapped_chain.pkl')
   return reduceMCMC(frameList)
