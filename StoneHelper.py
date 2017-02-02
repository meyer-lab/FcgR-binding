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
import StoneModel
import importlib

try:
   import cPickle as pickle
except:
   import pickle

importlib.reload(StoneModel)

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

Rquant = StoneModel.StoneModel().Rquant

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

def makeFcIgLegend():
    patches = list()

    for f in FcgRs:
        patches.append(mpatches.Patch(color=FcgRs[f], label=f))

    for j in Igs:
        patches.append(mlines.Line2D([], [], color='black', marker=Igs[j], markersize=7, label=j, linestyle='None'))

    return patches

def plotNormalizedBindingvsKA(fitMean, ax1=None, ax2=None, backGray=True):
    # Select the subset of data we want
    fitMean = fitMean[['Ig', 'TNP', 'FcgR', 'Ka', 'Meas_mean', 'Meas_std', 'Expression_mean']]

    # Normalize the binding data to expression
    fitMean = fitMean.assign(Meas_mean = fitMean['Meas_mean'] / fitMean['Expression_mean'] * 1.0E4)
    fitMean = fitMean.assign(Meas_std = fitMean['Meas_std'] / fitMean['Expression_mean'] * 1.0E4)

    fitMean = fitMean.as_matrix()
    if ax1 == None:
        fig = plt.figure(figsize=(9,5))
        ax1 = fig.add_subplot(1, 2, 1)

    mfcVal = 'None'
    for j in range(len(Igs)):
        for k in range(len(FcgRs)):
            ax1.errorbar(fitMean[8*j+k][3],fitMean[8*j+k][4],yerr=fitMean[8*j+k][5],marker=Igs[igs[j]],mfc=mfcVal,mec=FcgRs[fcgrs[k]],ecolor=FcgRs[fcgrs[k]],linestyle='None')

    ax1.set_xscale('log')
    plt.ylabel('Measured TNP-4 binding')
    plt.xlabel('FcgR-IgG Ka')

    if ax2 == None:
        ax2 = fig.add_subplot(1, 2, 2)

    for j in range(len(Igs)):
        for k in range(len(FcgRs)):
            mfcVal = FcgRs[fcgrs[k]]
            ax2.errorbar(fitMean[8*j+k+4][3],fitMean[8*j+k+4][4],yerr=fitMean[8*j+k+4][5],marker=Igs[igs[j]],mfc=mfcVal,mec=FcgRs[fcgrs[k]],ecolor=FcgRs[fcgrs[k]],linestyle='None')

    ax2.legend(handles=makeFcIgLegend(), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    ax2.set_xscale('log')
    plt.xlabel('FcgR-IgG Ka')
    if backGray:
        ax1.set_facecolor(backColor)
        ax2.set_facecolor(backColor)

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

def mfiAdjMeanFigureMaker(StoneM, axarr=None, ylabelfontsize=14, subtitlefontsize=16, legbbox=(2,1), tnpbsafontsize=10, titlefontsize=18, titlePos=(-3,6), backGray=True):
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
    colorz = [colors[3],colors[0],colors[4],colors[1]]
    species = [r'Fc$\gamma$RIA', r'Fc$\gamma$RIIA-131R', r'Fc$\gamma$RIIA-131H',
            r'Fc$\gamma$RIIB', r'Fc$\gamma$RIIIA-158F', r'Fc$\gamma$RIIIA-158V']

    units = int((3*width+len(ind)-1)/0.25)
    tnpbsaLabels = ['']*int((3*width+len(ind)-1)/0.25)
    tnpbsaLabels.insert(4,'TNP-4-BSA')
    tnpbsaLabels.insert(14,'TNP-26-BSA')

    ## Generate a figure with a 2 X 4 array of subplots; the rightmost column exists
    ## only as a place to put the legend. The axes of these rightmost plots are whited
    ## out for de-facto invisibility.
    if axarr == None:
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
            rects.append(axarr[j].bar(ind,temp,width,color=colorz[k],yerr=stds,error_kw=dict(elinewidth=2,ecolor='black')))
        for k in range(4):
            temp = [0]*N
            temp.remove(0)
            temp.insert(5+k,np.nanmean(mfiAdjMean[4*(j-1)+k][5:8]))
            stds = [0]*N
            stds.remove(0)
            stds.insert(5+k,np.nanstd(mfiAdjMean[4*(j-1)+k][5:8]))
            rects.append(axarr[j].bar(ind,temp,width,color=colorz[k],yerr=stds,error_kw=dict(elinewidth=2,ecolor='black')))

    # axes and labels
    for j in range(6):
        axarr[j].set_xlim(-0.5*width,len(ind)-1+1.5*width)
        axarr[j].xaxis.set_ticks(np.arange(-0.5*width,len(ind)-1+2.5*width,0.5))
        axarr[j].set_xticklabels(tnpbsaLabels,fontproperties=FontProperties(size=tnpbsafontsize))
        axarr[j].tick_params(axis='x', length=0)
        axarr[j].grid(b=False)
        axarr[j].set_ylim(0,5)
        if j%3 == 0:
            axarr[j].set_ylabel('maMFIs',fontsize=ylabelfontsize)
        axarr[j].set_title(species[j],fontsize=subtitlefontsize)

    ## Add a legend denoting IgG species
    leg = axarr[2].legend((rects[i][0] for i in range(4)),('IgG'+str(i+1) for i in range(4)),bbox_to_anchor=legbbox)

    ## Set axeses facecolors, if backGray
    if backGray:
        for ax in axarr:
            ax.set_facecolor(backColor)

def FcgRQuantificationFigureMaker(StoneM, ax=None, ylabelfontsize=14, titlefontsize=18, legbbox=(2,1), backGray=True, legend=True):
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
    ax.set_ylabel('Number of Receptors',fontsize=ylabelfontsize)
    if backGray:
        ax.set_facecolor(backColor)

    ## Create legend
    if legend:
        leg = ax.legend((rects[j][0] for j in range(N)),(r'Fc$\gamma$R'+species[j] for j in range(N)),bbox_to_anchor=legbbox)

def histSubplots(axes=None,tight_layout=False,backGray=True):
    if axes == None:
        fig, axes = plt.subplots(nrows=3, ncols=2)

    dset[['Kx1'     ]].plot.hist(ax=axes[0,0], bins = 100, color=colors[0])
    dset[['sigConv1', 'sigConv2']].plot.hist(ax=axes[0,1], bins = 100, color=[colors[j] for j in range(2)])
    dset[['gnu1', 'gnu2'        ]].plot.hist(ax=axes[1,0], bins = 100, color=[colors[j] for j in range(2)])
    dset[['sigma', 'sigma2'     ]].plot.hist(ax=axes[1,1], bins = 100, color=[colors[j] for j in range(2)])

    RexpBoxplot(axes[2,0])

##    temp = dset[['Rexp']].values
##    for j in range(temp.shape[1]):
##       y = np.array([-j+5]*temp.shape[0])
##    axes[2,0].set_ylim(0,12000)
##    print(good)
    a = 1e3
    b = 1e5
    c = 1e3
    d = 1e5
##    h, l = axes[2,0].get_legend_handles_labels()
##    h[0].get_bbox().set_points([[a,b],[c,d]])
    ##print(h[0].get_bbox().get_points())

    if tight_layout:
        plt.tight_layout()
    if backGray:
        for elem in axes:
            for ax in elem:
                ax.set_facecolor(backColor)
    plt.show()

def RexpBoxplot(ax=None):
    if ax == None:
        ax = plt.gca()
    objs = ax.boxplot(10**dset[['Rexp']].as_matrix(),whis=[5,95],sym='')
    for j in range(int(len(objs['caps'])/2)):
        objs['caps'][2*j].set_color(FcgRs[fcgrs[j]])
        objs['caps'][2*j+1].set_color(FcgRs[fcgrs[j]])
        objs['boxes'][j].set_color(FcgRs[fcgrs[j]])
        objs['medians'][j].set_color(FcgRs[fcgrs[j]])
        objs['whiskers'][2*j].set_color(FcgRs[fcgrs[j]])
        objs['whiskers'][2*j+1].set_color(FcgRs[fcgrs[j]])
        for elem in Rquant[j]:
            ax.plot(j+1,10**elem,color=FcgRs[fcgrs[j]],marker='x')
    ax.semilogy()
    ax.set_xticks([])
    ax.set_ylabel(ylabel='Number of Receptors Expressed')

def sigmaNuHists(axes=None,tight_layout=False,backGray=True):
    if axes == None:
        fig, axes = plt.subplots(nrows=2, ncols=1)
    newdset = dset
    newdset = newdset.assign(sigDiff = lambda x: np.power(10, x.sigConv2 - x.sigConv1))
    newdset = newdset.assign(gnuDiff = lambda x: x.gnu2 / x.gnu1)
    newdset['sigDiff'].plot.hist(ax=axes[0], bins = 100).set_xlabel(r'$\frac{\sigma^*_{26}}{\sigma^*_4}$',fontsize=16)
    newdset['gnuDiff'].plot.hist(ax=axes[1], bins = 20).set_xlabel(r'$\frac{\nu_{26}}{\nu_4}$',fontsize=16)
    if backGray:
        for ax in axes:
            ax.set_facecolor(backColor)
    if tight_layout:
        plt.tight_layout()
    plt.show()

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

def violinTest(ax=None):
    if ax == None:
        ax = plt.gca()
    for j in range(len(FcgRs)):
        toplot = np.full(dset[['Rexp']].values.shape,0.0)
        toplot[:][j] = dset[['Rexp']].values[:][j]
        objs = sns.violinplot(data=toplot,color=colors[0],ax=ax)
    ax.set_xticks([])
    ax.semilogy()
    print(objs)
    plt.show()
