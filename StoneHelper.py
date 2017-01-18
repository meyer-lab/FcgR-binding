import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib import rc
from matplotlib.font_manager import FontProperties
import h5py
from tqdm import tqdm

try:
   import cPickle as pickle
except:
   import pickle

def rep(x, N):
  return [item for item in x for i in range(N)]

Igs = {'IgG1':'o', 'IgG2':'d', 'IgG3':'s', 'IgG4':'^'}

FcgRs = {'FcgRI':'black', 'FcgRIIA-Arg':'blue',
          'FcgRIIIA-Phe':'green', 'FcgRIIIA-Val':'red',
          'FcgRIIA-His':'orange', 'FcgRIIB':'gray'}

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
    for ii in tqdm(range(pSet.shape[0])):
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

def makeFcIgLegend():
    patches = list()

    for f in FcgRs:
        patches.append(mpatches.Patch(color=FcgRs[f], label=f))

    for j in Igs:
        patches.append(mlines.Line2D([], [], color='black', marker=Igs[j], markersize=7, label=j, linestyle='None'))

    return patches

def plotNormalizedBindingvsKA(fitMean, ax1=None, ax2=None):
    # Select the subset of data we want
    fitMean = fitMean[['Ig', 'TNP', 'FcgR', 'Ka', 'Meas_mean', 'Meas_std', 'Expression_mean']]

    # Normalize the binding data to expression
    fitMean = fitMean.assign(Meas_mean = fitMean['Meas_mean'] / fitMean['Expression_mean'] * 1.0E4)
    fitMean = fitMean.assign(Meas_std = fitMean['Meas_std'] / fitMean['Expression_mean'] * 1.0E4)

    if ax1 == None:
        fig = plt.figure(figsize=(9,5))
        ax1 = fig.add_subplot(1, 2, 1)

    for j in Igs:
        for f in FcgRs:
            temp = fitMean[fitMean['Ig'] == j]
            temp = temp[temp['FcgR'] == f]

            temp = temp[temp['TNP'] == 'TNP-4']
            mfcVal = 'None'

            ax1.errorbar(temp['Ka'], temp['Meas_mean'],
                        yerr = temp['Meas_std'], marker = Igs[j],
                        mfc = mfcVal, mec = FcgRs[f], ecolor = FcgRs[f], linestyle = 'None')

    ax1.set_xscale('log')
    plt.ylabel('Measured TNP-4 binding')
    plt.xlabel('FcgR-IgG Ka')

    if ax2 == None:
        ax2 = fig.add_subplot(1, 2, 2)

    for j in Igs:
        for f in FcgRs:
            temp = fitMean[fitMean['Ig'] == j]
            temp = temp[temp['FcgR'] == f]

            temp = temp[temp['TNP'] != 'TNP-4']
            mfcVal = FcgRs[f]

            ax2.errorbar(temp['Ka'], temp['Meas_mean'],
                        yerr = temp['Meas_std'], marker = Igs[j],
                        mfc = mfcVal, mec = FcgRs[f], ecolor = FcgRs[f], linestyle = 'None')

    ax2.legend(handles=makeFcIgLegend(), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    ax2.set_xscale('log')
    plt.xlabel('FcgR-IgG Ka')

def plotFit(fitMean,ax=None):
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

                ax.errorbar(temp['Fit'], temp['Meas_mean']+0.01,
                            yerr = temp['Meas_std'], marker = Igs[j],
                            mfc = mfcVal, mec = color, ecolor = color,
                            linestyle = 'None')

    ax.legend(handles=makeFcIgLegend(), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot([0.08, 10], [0.08, 10])
    ax.set_ylim(0.01, 10)
    ax.set_xlim(0.08, 70)
    plt.xlabel('Fitted prediction')
    plt.ylabel('Measured ligand binding')


def plotQuant(fitMean, nameFieldX, nameFieldY, ax=None):
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

    #ax.legend(handles=makeFcIgLegend())

    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.ylabel(nameFieldY)
    plt.xlabel(nameFieldX)

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

def mfiAdjMeanFigureMaker(StoneM, f=None):
    ## Use LaTex to render text; though usetex is input as False, it causes LaTex to be used.
    ## Inputting usetex = True causes an error; this is a bug I found online
    ## (http://matplotlib.1069221.n5.nabble.com/tk-pylab-and-unicode-td10458.html)
    rc('text',usetex=False)

    ## Our data
    mfiAdjMean = StoneM.mfiAdjMean

    ## Number of bars, including an "empty" bar between TNP-4-BSA and TNP-26-BSA data
    N = 9

    ind = np.arange(N)
    ## Width of bars
    width = 0.5

    ## Setting up strings useful for plotting
    colors = ['red','blue','green','yellow']
    species = [r'Fc$\gamma$RIA', r'Fc$\gamma$RIIA-131R', r'Fc$\gamma$RIIA-131H',
            r'Fc$\gamma$RIIB', r'Fc$\gamma$RIIIA-158F', r'Fc$\gamma$RIIIA-158V']

    units = int((3*width+len(ind)-1)/0.25)
    tnpbsaLabels = ['']*int((3*width+len(ind)-1)/0.25)
    tnpbsaLabels.insert(4,'TNP-4-BSA')
    tnpbsaLabels.insert(14,'TNP-26-BSA')

    ## Generate a figure with a 2 X 4 array of subplots; the rightmost column exists
    ## only as a place to put the legend. The axes of these rightmost plots are whited
    ## out for de-facto invisibility.
    if f == None:
        f = plt.figure()
    axarr = []
    for j in range(6):
       exec('axarr.append(f.add_subplot(24'+str(int(j+1+np.floor(j/3)))+'))')

    ## Plotting mfiAdjMean
    for j in range(6):
        rects = []
        for k in range(4):
            temp = [0]*N
            temp.remove(0)
            temp.insert(k,np.nanmean(mfiAdjMean[4*(j-1)+k][1:4]))
            stds = [0]*N
            stds.remove(0)
            stds.insert(k,np.nanstd(mfiAdjMean[4*(j-1)+k][1:4]))
            rects.append(axarr[j].bar(ind,temp,width,color=colors[k],yerr=stds,error_kw=dict(elinewidth=2,ecolor='black')))
        for k in range(4):
            temp = [0]*N
            temp.remove(0)
            temp.insert(5+k,np.nanmean(mfiAdjMean[4*(j-1)+k][5:8]))
            stds = [0]*N
            stds.remove(0)
            stds.insert(5+k,np.nanstd(mfiAdjMean[4*(j-1)+k][5:8]))
            rects.append(axarr[j].bar(ind,temp,width,color=colors[k],yerr=stds,error_kw=dict(elinewidth=2,ecolor='black')))

    # axes and labels
    for j in range(6):
        axarr[j].set_xlim(-0.5*width,len(ind)-1+1.5*width)
        axarr[j].xaxis.set_ticks(np.arange(-0.5*width,len(ind)-1+2.5*width,0.5))
        axarr[j].set_xticklabels(tnpbsaLabels,fontproperties=FontProperties(size=10))
        axarr[j].tick_params(axis='x', length=0)
        axarr[j].grid(b=False)
        axarr[j].set_ylim(0,5)
        if j%3 == 0:
            axarr[j].set_ylabel('maMFIs',fontsize=14)
        axarr[j].set_title(species[j],fontsize=16)

    ## Add a legend denoting IgG species
    leg = axarr[2].legend((rects[i][0] for i in range(4)),('IgG'+str(i+1) for i in range(4)),bbox_to_anchor=(2,1))

    ## Set title for the set of plots
    if StoneM.newData:
        titleEnd = ' (New Data)'
    else:
        titleEnd = ' (Old Data)'
    f.suptitle('Mean-Adjusted MFIs'+titleEnd,fontsize=18)

    ## Show figure
    plt.show()

def FcgRQuantificationFigureMaker(StoneM,ax=None):
    ## Please see comments from mfiAdjMeanFigureMaker
    rc('text',usetex=False)

    Rquant = StoneM.Rquant

    ## Number of bars
    N = len(Rquant)
    ## Relative width of bars
    width = 0.5
    ## List of 6 tuples, one tuple per FcgR species. The tuple's first element is the
    ## (nan)mean expression for that species, while the second element is the (nan)std
    ## of the distribution of receptor expressions measured
    iterable = [(np.nanmean(10**Rquant[j]),np.nanstd(10**Rquant[j])) for j in range(N)]

    ## Set up strings necessary for the coloring and the legend
    ind = np.arange(N)
    colors = ['red','orange','yellow','green','blue','purple']
    species = ['IA','IIA-131R','IIA-131H','IIB','IIIA-158F','IIIA-158V']

    ## Create bars and error bars per species
    if ax == None:
        f = plt.figure()
        ax = f.add_subplot(121)
    rects = []
    for j in range(N):
        temp = [0]*(N-1)
        temp.insert(j,iterable[j][0])
        stds = [0]*(N-1)
        stds.insert(j,iterable[j][1])
        rects.append(ax.bar(ind,temp,color=colors[j],yerr=stds,error_kw=dict(elinewidth=2,ecolor='black')))

    ## Set up axes
    ax.xaxis.set_visible(False)
    ax.set_xlim(-0.5*width,len(ind)+0.2*width)
    ax.tick_params(axis='x',length=0)
    ax.grid(b=False)
    ax.set_yscale('log')
    ax.set_ylabel('Number of Receptors',fontsize=14)

    f = ax.get_figure()
    f.suptitle('Receptor Quantification by Receptor Species',fontsize=18)

    ## Create legend
    leg = ax.legend((rects[j][0] for j in range(N)),(r'Fc$\gamma$R'+species[j] for j in range(N)),bbox_to_anchor=(2,1))

    ## Show figure
    plt.show()
