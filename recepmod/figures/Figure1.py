import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
from ..StoneModel import StoneModel
from ..StoneHelper import getFitMeasSummarized
from .FigureCommon import *

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

def makeFigure():
    StoneM = StoneModel()

    f = plt.figure(figsize=(8.5,11))
    gs1 = gridspec.GridSpec(2,3,height_ratios=[1,3],width_ratios=[2,3,3])
    ax = f.add_subplot(gs1[0])
    FcgRQuantificationFigureMaker(StoneM,ax,legbbox=(1.75,1),titlefontsize=16)
    ax2 = f.add_subplot(gs1[1])
    ax3 = f.add_subplot(gs1[2])

    fitMean = getFitMeasSummarized(StoneM)

    plotNormalizedBindingvsKA(fitMean, ax2, ax3)
    gs2 = gridspec.GridSpec(8,4,height_ratios=[1,1,1,1,1,4,1,4])
    axarr = []
    for j in range(6):
        axarr.append(f.add_subplot(gs2[20+j+5*int(np.floor(j/3))]))
    mfiAdjMeanFigureMaker(StoneM,axarr,legbbox=(1.5,1),tnpbsafontsize=12)

    return f
