import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import seaborn as sns
import pandas as pd
from ..StoneModel import StoneModel
from ..StoneHelper import getFitMeasSummarized, getMeasuredDataFrame
from .FigureCommon import Igs, FcgRidx, makeFcIgLegend, subplotLabel, FcgRidxL

def plotNormalizedBindingvsKA(fitMean, ax1=None, ax2=None, ylabelpad=-0.3, ytickx=0.08):
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
        for _, row in data.iterrows():
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
        axInt.set_ylabel('Measured TNP-BSA binding',labelpad=ylabelpad)
        axInt.set_ylim(1.0E-3, 1.0E-1)

    plotF(ax1, fitMean.loc[fitMean['TNP'] == "TNP-4",:])
    plotF(ax2, fitMean.loc[fitMean['TNP'] == "TNP-26",:])

    ax1.set_title('TNP-4-BSA')
    ax2.set_title('TNP-26-BSA')

    for elem in ax1.get_yticklabels():
        elem.set_x(ytickx)
    for elem in ax2.get_yticklabels():
        elem.set_x(ytickx)

def plotAvidityEffectVsKA(fitMean, ax1=None, ylabelpad=-0.3, ytickx = 0.08):
    # Make axes if none exist
    if ax1 is None:
        ax1 = plt.figure().add_subplot(121)

    # Select the subset of data we want
    fitMean = fitMean[['Ig', 'TNP', 'FcgR', 'Ka', 'Meas_mean', 'Meas_std']]

    # Reorder dataframe for processing
    fitMean = pd.pivot_table(fitMean, index = ['Ig', 'FcgR', 'Ka'], columns = ['TNP'])

    # Calculate the ratio of binding and error
    rratio = fitMean[('Meas_mean', 'TNP-26')] / fitMean[('Meas_mean', 'TNP-4')]
    sstd = rratio * np.sqrt(np.power(fitMean[('Meas_std', 'TNP-26')]/fitMean[('Meas_mean', 'TNP-26')], 2) + np.power(fitMean[('Meas_std', 'TNP-4')]/fitMean[('Meas_mean', 'TNP-4')], 2))

    fitMean = fitMean.assign(Ratio = rratio, STD = sstd)

    # Reset index
    fitMean = fitMean.reset_index()
    fitMean.columns = fitMean.columns.droplevel(1)

    for _, row in fitMean.iterrows():
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
    ax1.set_ylabel('TNP-26 / TNP-4 Binding',labelpad=ylabelpad)
    for j in range(6):
        ax1.get_yticklabels()[j].set_x(ytickx)
    ax1.set_ylim(1, 20)

    ax1.legend(handles=makeFcIgLegend(), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


def FcgRQuantificationFigureMaker(StoneM, ax=None, ylabelpad=0, ytickx=0):
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
    axx.set_ylabel("Receptors/Cell", labelpad=ylabelpad)
    ax.set_xlabel("")
    axx.set_xlabel("")
    for elem in axx.get_yticklabels():
        elem.set_x(ytickx)
    axx.set_xticklabels(axx.get_xticklabels(), rotation=40, rotation_mode="anchor", ha="right")

def mfiAdjMeanFigureMaker(measAll, axarr=None):
    if axarr is None:
        f = plt.figure()

        # Make grid
        gs1 = gridspec.GridSpec(2,3)

        # Create 6 axes for each FcgR
        axarr = [ f.add_subplot(gs1[x]) for x in range(6) ]

    fcIter = zip(axarr, FcgRidx.keys())

    # Loop through receptors creating plot
    for axx, fcr in fcIter:
        sns.barplot(x="Ig",
                    y = "Meas",
                    hue="TNP",
                    data=measAll.loc[measAll['FcgR'] == fcr,:],
                    ax = axx,
                    ci = 68)

        axx.set_ylabel("Binding (RU)")
        axx.set_xlabel("")
        axx.legend_.remove()
        axx.set_title(fcr)

def makeFigure():
    StoneM = StoneModel()

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    f = plt.figure(figsize=(7,6))
    gs1 = gridspec.GridSpec(3,8,height_ratios=[4,1,6],width_ratios=[20,4,20,4,20,4,20,16])
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

    ax4 = f.add_subplot(gs1[6])
    plotAvidityEffectVsKA(fitMean,ax4)

    subplotLabel(ax4, 'D')

    gs2 = gridspec.GridSpec(8,5,height_ratios=[4,4,4,6,8,12,7,12],width_ratios=[4,1,4,1,4])
    axarr = []
    for j in range(6):
        axarr.append(f.add_subplot(gs2[25+2*j+4*int(np.floor(j/3))]))

    subplotLabel(axarr[0], 'E')

    mfiAdjMeanFigureMaker(measAll,axarr)

    gs3 = gridspec.GridSpec(4,3,height_ratios=[26,12,6,6],width_ratios=[15,2,5])

    return f
