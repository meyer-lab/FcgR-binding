import matplotlib.pyplot as plt
from matplotlib import gridspec, rcParams
import numpy as np
import seaborn as sns
import pandas as pd
from ..StoneModel import StoneModel
from ..StoneHelper import getFitMeasSummarized, getMeasuredDataFrame
from .FigureCommon import Igs, FcgRidx, makeFcIgLegend, subplotLabel, FcgRidxL

# TODO: Add a line on top of the MFI vs. Ka plots of the monovalent binding

def plotNormalizedBindingvsKA(fitMean, ax1=None, ax2=None):
    # Select the subset of data we want
    fitMean = fitMean[['Ig', 'TNP', 'FcgR', 'Ka', 'Meas_mean', 'Meas_std', 'Expression_mean']]

    # Normalize the binding data to expression
    fitMean = fitMean.assign(Meas_mean = fitMean['Meas_mean'] / fitMean['Expression_mean'] * 1.0E4)
    fitMean = fitMean.assign(Meas_std = fitMean['Meas_std'] / fitMean['Expression_mean'] * 1.0E4)

    if ax1 is None or ax2 is None:
        fig = plt.figure(figsize=(9,5))
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)

    def plotF(axInt, data):
        for index, row in data.iterrows():
            colorr = FcgRidx[row['FcgR']]
            axInt.errorbar(x=row['Ka'],
                        y=row['Meas_mean'],
                        yerr=row['Meas_std'],
                        marker=Igs[row['Ig']],
                        mfc=colorr,
                        mec=colorr,
                        ms=5,
                        ecolor=colorr,
                        linestyle='None')

        axInt.loglog()
        axInt.set_xlabel(r'Fc$\gamma$R-IgG Ka')
        axInt.set_ylabel('Measured TNP-BSA binding')
        axInt.set_ylim(1.0E-3, 1.0E-1)

    plotF(ax1, fitMean.loc[fitMean['TNP'] == "TNP-4",:])
    plotF(ax2, fitMean.loc[fitMean['TNP'] == "TNP-26",:])

    ax1.set_title('TNP-4-BSA')
    ax2.set_title('TNP-26-BSA')

    ax2.legend(handles=makeFcIgLegend(), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

def plotAvidityEffectVsKA(fitMean, ax1=None):
    # Make axes if none exist
    if ax1 is None:
        ax1 = plt.figure().add_subplot(121)

    # Select the subset of data we want
    fitMean = fitMean[['Ig', 'TNP', 'FcgR', 'Ka', 'Meas_mean', 'Meas_std']]

    # Reorder dataframe for processing
    fitMean = pd.pivot_table(fitMean, index = ['Ig', 'FcgR', 'Ka'], columns = ['TNP'])

    # Calculate the ratio of binding
    fitMean = fitMean.assign(Ratio = fitMean[('Meas_mean', 'TNP-26')] / fitMean[('Meas_mean', 'TNP-4')])

    # Calculate the error in the ratio
    fitMean = fitMean.assign(STD = fitMean['Ratio'] * np.sqrt(np.power(fitMean[('Meas_std', 'TNP-26')]/fitMean[('Meas_mean', 'TNP-26')], 2) + np.power(fitMean[('Meas_std', 'TNP-4')]/fitMean[('Meas_mean', 'TNP-4')], 2)))

    # Reset index
    fitMean = fitMean.reset_index()
    fitMean.columns = fitMean.columns.droplevel(1)

    for index, row in fitMean.iterrows():
        colorr = FcgRidx[row['FcgR']]
        ax1.errorbar(x=row['Ka'],
                    y=row['Ratio'],
                    yerr=row['STD'],
                    marker=Igs[row['Ig']],
                    mfc=colorr,
                    mec=colorr,
                    ms=5,
                    ecolor=colorr,
                    linestyle='None')

    ax1.loglog()
    ax1.set_xlabel(r'Fc$\gamma$R-IgG Ka')
    ax1.set_ylabel('TNP-26 / TNP-4 Binding')
    ax1.set_ylim(1, 20)

    ax1.legend(handles=makeFcIgLegend(), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


def FcgRQuantificationFigureMaker(StoneM, ax=None):
    # Put receptor expression measurements into a dataframe
    df = pd.DataFrame(StoneM.Rquant).T

    # Assign the names of the receptors
    df.columns = FcgRidxL.keys()

    # Melt the dataframe
    dfm = pd.melt(df)

    # Remove nan values and transform to absolute scale
    dfm = dfm[np.isfinite(dfm['value'])]
    dfm['value'] = dfm['value'].apply(lambda x: np.power(10,x))

    ## Create bars and error bars per species
    if ax is None:
        ax = plt.figure().add_subplot(121)

    # Plot everything
    axx = sns.barplot(x = "variable", y = "value", data = dfm, ax = ax)

    ## Set up axes
    axx.set_yscale('log')
    axx.set_ylim(1.0E5, 1.0E7)
    axx.set_ylabel("Number of Receptors")
    ax.set_xlabel("")
    axx.set_xlabel("")
    axx.set_xticklabels(axx.get_xticklabels(), rotation=40, rotation_mode="anchor", ha="right")

def mfiAdjMeanFigureMaker(measAll, axarr=None):
    if axarr is None:
        f = plt.figure()

        # Make grid
        gs1 = gridspec.GridSpec(2,3)

        # Create 6 axes for each FcgR
        axarr = [ f.add_subplot(gs1[x]) for x in range(6) ]

    fcIter = zip(axarr, FcgRidx.keys())

    # TODO: Redo this code using seaborn
    # What's below here isn't at all correct, but is a placeholder to provide
    # some idea
    for axx, fcr in fcIter:
        sns.barplot(x="Ig",
                    y = "Meas",
                    hue="TNP",
                    data=measAll.loc[measAll['FcgR'] == fcr,:],
                    ax = axx,
                    ci = 68)

        axx.legend_.remove()
        axx.set_title(fcr)

def makeFigure():
    StoneM = StoneModel()

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    f = plt.figure(figsize=(7,6))
    gs1 = gridspec.GridSpec(3,6,height_ratios=[4,1,6],width_ratios=[16,4,20,4,20,0])
    ax = f.add_subplot(gs1[0])
    FcgRQuantificationFigureMaker(StoneM,ax)

    subplotLabel(ax, 'A')

    ax2 = f.add_subplot(gs1[2])
    ax3 = f.add_subplot(gs1[4])

    fitMean = getFitMeasSummarized(StoneM)
    measAll = getMeasuredDataFrame(StoneM)

    plotNormalizedBindingvsKA(fitMean, ax2, ax3)

    subplotLabel(ax2, 'B')
    subplotLabel(ax3, 'C')

    gs2 = gridspec.GridSpec(8,7,height_ratios=[4,4,4,6,8,12,7,12],width_ratios=[4,1,4,1,4,1,5])
    axarr = []
    for j in range(6):
        axarr.append(f.add_subplot(gs2[35+2*j+8*int(np.floor(j/3))]))

    subplotLabel(axarr[0], 'D')

    mfiAdjMeanFigureMaker(measAll,axarr)

    gs3 = gridspec.GridSpec(4,3,height_ratios=[26,12,6,6],width_ratios=[15,2,5])
    ax4 = f.add_subplot(gs3[5])
    plotAvidityEffectVsKA(fitMean,ax4)

    subplotLabel(ax4, 'E')
    
    return f
