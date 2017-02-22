import matplotlib.pyplot as plt
from matplotlib import gridspec, rcParams
import numpy as np
from ..StoneModel import StoneModel
from ..StoneHelper import getFitMeasSummarized
from .FigureCommon import *
import seaborn as sns

def plotNormalizedBindingvsKA(fitMean, ax1=None, ax2=None, legfontsize=10):
    # Select the subset of data we want
    fitMean = fitMean[['Ig', 'TNP', 'FcgR', 'Ka', 'Meas_mean', 'Meas_std', 'Expression_mean']]

    # Normalize the binding data to expression
    fitMean = fitMean.assign(Meas_mean = fitMean['Meas_mean'] / fitMean['Expression_mean'] * 1.0E4)
    fitMean = fitMean.assign(Meas_std = fitMean['Meas_std'] / fitMean['Expression_mean'] * 1.0E4)

    fitMean = fitMean.as_matrix()
    if ax1 == None or ax2 == None:
        fig = plt.figure(figsize=(9,5))
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)

    mfcVal = 'None'
    for j in range(len(Igs)):
        for k in range(len(FcgRs)):
            ax1.errorbar(fitMean[8*j+k][3],fitMean[8*j+k][4],yerr=fitMean[8*j+k][5],marker=Igs[igs[j]],mfc=mfcVal,mec=FcgRs[fcgrs[k]],ecolor=FcgRs[fcgrs[k]],linestyle='None')

    ax1.set_xscale('log')
    ax1.set_ylabel('Measured TNP-BSA binding')
    ax1.set_xlabel(r'Fc$\gamma$R-IgG Ka')
    ax2.set_xlabel(r'Fc$\gamma$R-IgG Ka')

    for j in range(len(Igs)):
        for k in range(len(FcgRs)):
            mfcVal = FcgRs[fcgrs[k]]
            ax2.errorbar(fitMean[8*j+k+4][3],fitMean[8*j+k+4][4],yerr=fitMean[8*j+k+4][5],marker=Igs[igs[j]],mfc=mfcVal,mec=FcgRs[fcgrs[k]],ecolor=FcgRs[fcgrs[k]],linestyle='None')

    ax2.legend(handles=makeFcIgLegend(), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize=legfontsize)
    ax2.set_xscale('log')

def FcgRQuantificationFigureMaker(StoneM, ax=None):
    # Put receptor expression measurements into a dataframe
    df = pd.DataFrame(StoneM.Rquant).T

    # Assign the names of the receptors
    df.columns = fcgrs

    # Melt the dataframe
    dfm = pd.melt(df)

    # Remove nan values and transform to absolute scale
    dfm = dfm[np.isfinite(dfm['value'])]
    dfm['value'] = dfm['value'].apply(lambda x: np.power(10,x))

    ## Create bars and error bars per species
    if ax == None:
        ax = plt.figure().add_subplot(121)

    # Plot everything
    axx = sns.barplot(x = "variable", y = "value", data = dfm, ax = ax)

    ## Set up axes
    axx.set_yscale('log')
    axx.set_ylim(1.0E5, 1.0E7)
    axx.set_ylabel("Number of Receptors")
    ax.set_xlabel("")
    axx.set_xlabel("")
    axx.set_xticklabels(axx.get_xticklabels(),rotation=90)

def mfiAdjMeanFigureMaker(StoneM, axarr=None, ylabelfontsize=14, subtitlefontsize=16, legbbox=(2,1), tnpbsafontsize=10, titlefontsize=18, titlePos=(-3,6), legfontsize=10):
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
##    for j in range(6):
##        rects = []
##        for k in range(4):
##            temp = [0]*N
##            temp.remove(0)
##            temp.insert(k,np.nanmean(mfiAdjMean[4*(j-1)+k][1:4]))
##            stds = [0]*N
##            stds.remove(0)
##            stds.insert(k,np.nanstd(mfiAdjMean[4*(j-1)+k][1:4]))
##            rects.append(axarr[j].bar(ind,temp,width,color=colors[k],yerr=stds,error_kw=dict(elinewidth=2,ecolor='black')))
##        for k in range(4):
##            temp = [0]*N
##            temp.remove(0)
##            temp.insert(5+k,np.nanmean(mfiAdjMean[4*(j-1)+k][5:8]))
##            stds = [0]*N
##            stds.remove(0)
##            stds.insert(5+k,np.nanstd(mfiAdjMean[4*(j-1)+k][5:8]))
##            rects.append(axarr[j].bar(ind,temp,width,color=colors[k],yerr=stds,error_kw=dict(elinewidth=2,ecolor='black')))
    for j in range(6):
        rects = []
        temp = [[0]]*N
        for k in range(4):
            temp.insert(k,[np.nanmean(mfiAdjMean[4*(j-1)+k][1:4])])
            temp.insert(5+k,[np.nanmean(mfiAdjMean[4*(j-1)+k][5:8])])
            #print(temp)
            #print(' ')
            if j == 6 and k == 4:
                for elem in temp:
                    a = 1
                    #print(elem)
##            rects.append(sns.barplot(data=temp,color=sns.set_palette(sns.color_palette(colors)),ax=axarr[j]))
        sns.barplot(data=temp,color=sns.set_palette('colorblind'),ax=axarr[j])

    # axes and labels
##    for j in range(6):
##        axarr[j].set_xlim(-0.5*width,len(ind)-1+1.5*width)
##        axarr[j].xaxis.set_ticks(np.arange(-0.5*width,len(ind)-1+2.5*width,0.5))
##        axarr[j].set_xticklabels(tnpbsaLabels,fontproperties=FontProperties(size=tnpbsafontsize))
##        axarr[j].tick_params(axis='x', length=0)
##        axarr[j].grid(b=False)
##        axarr[j].set_ylim(0,5)
##        if j%3 == 0:
##            axarr[j].set_ylabel('mean-adjusted MFIs',fontsize=ylabelfontsize)
##        axarr[j].set_title(species[j],fontsize=subtitlefontsize)

    ## Add a legend denoting IgG species
##    leg = axarr[2].legend((rects[i][0] for i in range(4)),('IgG'+str(i+1) for i in range(4)),bbox_to_anchor=legbbox,fontsize=legfontsize)

def makeFigure():
    StoneM = StoneModel()

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")
    rcParams['lines.markeredgewidth'] = 1.0

    f = plt.figure(figsize=(7,6))
    gs1 = gridspec.GridSpec(3,6,height_ratios=[4,1,6],width_ratios=[4,2,6,1,6,1])
    ax = f.add_subplot(gs1[0])
    FcgRQuantificationFigureMaker(StoneM,ax)

    subplotLabel(ax, 'A')

    ax2 = f.add_subplot(gs1[2])
    ax3 = f.add_subplot(gs1[4])

    fitMean = getFitMeasSummarized(StoneM)

    plotNormalizedBindingvsKA(fitMean, ax2, ax3, legfontsize=8)

    subplotLabel(ax2, 'B')
    subplotLabel(ax3, 'C')

    gs2 = gridspec.GridSpec(8,4,height_ratios=[1,1,1,1,1,4,1,4])
    axarr = []
    for j in range(6):
        axarr.append(f.add_subplot(gs2[20+j+5*int(np.floor(j/3))]))
    mfiAdjMeanFigureMaker(StoneM,axarr,legbbox=(1.75,1),tnpbsafontsize=7,subtitlefontsize=7,ylabelfontsize=7,legfontsize=7)

    return f
