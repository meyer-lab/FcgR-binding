"""
This creates Figure 1 which summarizes Anja's data.
"""

import matplotlib
matplotlib.use('AGG')
import numpy as np
import seaborn as sns
import pandas as pd
from .FigureCommon import Igs, Legend, FcgRidxL, FcgRidx, FcgRlist, FcgRlistL, IgList, texRename, iggRename


def plotNormalizedBindingvsKA(fitMean, ax1, ax2):
    # Select the subset of data we want
    fitMean = fitMean[['Ig', 'TNP', 'FcgR', 'Ka', 'Meas_mean', 'Meas_std', 'Expression_mean']]

    # Normalize the binding data to expression
    fitMean = fitMean.assign(Meas_mean = fitMean['Meas_mean'] / fitMean['Expression_mean'] * 1.0E4)
    fitMean = fitMean.assign(Meas_std = fitMean['Meas_std'] / fitMean['Expression_mean'] * 1.0E4)

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
        axInt.set_xlabel(r'hFc$\gamma$R-hIgG $K_a$')
        axInt.set_ylabel('Measured TNP-BSA Binding')
        axInt.set_ylim(1.0E-3, 1.0E-1)

    plotF(ax1, fitMean.loc[fitMean['TNP'] == "TNP-4",:])
    plotF(ax2, fitMean.loc[fitMean['TNP'] == "TNP-26",:])

    ax1.set_title('TNP-4-BSA')
    ax2.set_title('TNP-26-BSA')
    ax1.set_xlim(1E4, 1E8)
    ax1.set_xticks([1E4, 1E5, 1E6, 1E7, 1E8])
    ax2.set_xlim(1E4, 1E8)
    ax2.set_xticks([1E4, 1E5, 1E6, 1E7, 1E8])

def plotAvidityEffectVsKA(fitMean, ax1):

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

    # Mark IgGs as human
    fitMean['Ig'] = fitMean['Ig'].apply(iggRename)

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

    ax1.set_xscale('log', basex=10)
    ax1.set_yscale('log', basey=2)

    ax1.set_xlabel(r'hFc$\gamma$R-hIgG $K_a$')
    ax1.set_ylabel('TNP-26 / TNP-4 Binding')

    ax1.set_ylim(1, 20)
    ax1.set_yticks([1, 2, 4, 8, 16])

    ax1.set_xlim(1E4, 1E8)
    ax1.set_xticks([1E4, 1E5, 1E6, 1E7, 1E8])

    ax1.legend(handles=Legend(FcgRlistL, FcgRidxL,
                              [iggRename(igg) for igg in IgList], Igs),
               bbox_to_anchor=(1.6, 1.1), loc=2)


def FcgRQuantificationFigureMaker(StoneM, ax):
    # Put receptor expression measurements into a dataframe
    df = pd.DataFrame(StoneM.Rquant).T

    # Assign the names of the receptors
    df.columns = FcgRlistL

    # Melt the dataframe
    dfm = pd.melt(df)

    # Remove nan values and transform to absolute scale
    dfm = dfm[np.isfinite(dfm['value'])]
    dfm['value'] = dfm['value'].apply(lambda x: np.power(10,x))

    # Plot everything
    axx = sns.barplot(x = "variable", y = "value", data = dfm, ax = ax)

    ## Set up axes
    axx.set_yscale('log')
    axx.set_ylim(1.0E5, 1.0E7)
    axx.set_ylabel("Receptors/Cell")
    ax.set_xlabel("")
    axx.set_xlabel("")
    axx.set_xticklabels(axx.get_xticklabels(), rotation=40, rotation_mode="anchor", ha="right")
    # Change rectangle colors to those in FcgRidx
    for ii, child in enumerate(axx.get_children()[0:6]):
        child.set_edgecolor(FcgRidx[FcgRlist[ii]])
        child.set_facecolor(FcgRidx[FcgRlist[ii]])


def mfiAdjMeanFigureMaker(measAll, axarr):
    # Mark IgGs as human
    measAll['Ig'] = measAll['Ig'].apply(iggRename)

    fcIter = zip(axarr, FcgRlist)
    col = sns.crayon_palette(colors=['Tickle Me Pink', 'Brown'])
    # Loop through receptors creating plot
    for axx, fcr in fcIter:
        sns.barplot(x="Ig",
                    y="Meas",
                    hue="TNP",
                    data=measAll.loc[measAll['FcgR'] == fcr, :],
                    ax=axx,
                    ci=68)

        axx.set_ylabel("Normalized MFI")
        axx.set_xlabel("")
        axx.legend_.remove()
        axx.set_title(texRename(fcr))
        axx.set_xticklabels(axx.get_xticklabels(), rotation=40, rotation_mode="anchor", ha="right")
        # Change colors to make them different that in FcgRidx
        for ii, child in enumerate(axx.get_children()[0:8]):
            if ii < 4:
                child.set_facecolor(col[0])
                child.set_edgecolor(col[0])
            else:
                child.set_facecolor(col[1])
                child.set_edgecolor(col[1])

    axarr[2].legend(bbox_to_anchor=(1.6, 1), loc=2)


def makeFigure():
    from ..StoneModel import StoneModel
    from ..StoneHelper import getFitMeasSummarized, getMeasuredDataFrame
    from .FigureCommon import subplotLabel, getSetup

    StoneM = StoneModel()

    # Get list of axis objects
    ax, f = getSetup((7, 6), (3, 4))

    FcgRQuantificationFigureMaker(StoneM, ax[7])

    subplotLabel(ax[0], 'A')

    fitMean = getFitMeasSummarized(StoneM)
    measAll = getMeasuredDataFrame(StoneM)

    plotNormalizedBindingvsKA(fitMean, ax[8], ax[9])

    subplotLabel(ax[8], 'C')
    subplotLabel(ax[9], 'D')

    plotAvidityEffectVsKA(fitMean, ax[10])

    subplotLabel(ax[10], 'E')

    subplotLabel(ax[7], 'B')

    mfiAdjMeanFigureMaker(measAll, (ax[0], ax[1], ax[2], ax[4], ax[5], ax[6]))

    ax[3].axis('off')
    ax[11].axis('off')

    f.tight_layout()

    return f
