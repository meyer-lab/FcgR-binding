"""
This creates Figure 2 which fits the binding data to a model.
"""

import string
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
from .FigureCommon import Igs, FcgRidx, texRename, texRenameList, FcgRidxL, FcgRlist, FcgRlistL


def makeFigure():
    from ..StoneHelper import read_chain, getFitMeasMergedSummarized
    from .FigureCommon import getSetup, Legend, subplotLabel, iggRename, IgList

    # Retrieve model and fit from hdf5 file
    M, dset = read_chain()

    pBest = dset.iloc[np.argmax(dset['LL']), :][2:].as_matrix()

    # Get list of axis objects
    ax, f = getSetup((7, 6), (3, 3))

    # Blank out for the cartoon
    ax[0].axis('off')
    ax[0].legend(handles=Legend(FcgRlistL,
                                FcgRidxL,
                                [iggRename(igg) for igg in IgList], Igs),
                 loc=2,
                 bbox_to_anchor=(4.0, 1.0))

    # Show predicted versus actual
    plotFit(getFitMeasMergedSummarized(M, pBest), ax=ax[1])

    # Make Geweke diagnostic subplot
    GewekeDiagPlot(M, dset, ax[2])

    # Make histogram subplots
    histSubplots(dset, axes=[ax[3], ax[5], ax[6], ax[7]])

    # Plot the average avidity of binding
    AverageAvidity(ax[4])

    # Make receptor expression subplot
    violinPlot(dset, ax=ax[8])

    for ii, item in enumerate(ax):
        subplotLabel(item, string.ascii_uppercase[ii])

    # Try and fix overlapping elements
    f.tight_layout()

    return f


def violinPlot(dset, ax):
    from .FigureCommon import getRquant

    dset = dset[['Rexp']]
    dset.columns = FcgRlistL

    sns.violinplot(data=dset, cut=0, ax=ax, linewidth=0)

    ax.set_xticklabels(ax.get_xticklabels(),
                       rotation=40,
                       rotation_mode="anchor",
                       ha="right")

    ax.set_yticks([5, 6, 7])
    ax.set_yticklabels([r'$10^5$', r'$10^6$', r'$10^7$'])
    ax.set_ylabel(r'$\log_{10}$(Fc$\gamma$R Expression)')

    # Overlay FcgR quantifications
    for ii, row in enumerate(getRquant()):
        ax.plot([ii] * len(row), row, 'k_', mew=1.0)

    ax.set_ylim(5, 7)
    # Change violin colors to match FcgR colors in legend next to 2C
    for ii, child in enumerate(ax.get_children()[0:12]):
        if ii % 2 == 0:
            child.set_facecolor(FcgRidx[FcgRlist[int(ii / 2)]])
            child.set_edgecolor(FcgRidx[FcgRlist[int(ii / 2)]])


def histSubplots(dset, axes):
    dset.columns = texRenameList(dset.columns)

    dset[[texRename('Kx1')]].plot.hist(ax=axes[0], bins=20,
                                       color=[sns.color_palette()[0]], legend=False)
    dset[[texRename('sigConv1'), texRename('sigConv2')]].plot.hist(
        ax=axes[1], bins=20, color=sns.color_palette()[0:2])
    dset[[texRename('gnu1'), texRename('gnu2')]].plot.hist(ax=axes[2],
                                                           bins=np.arange(-0.5, 32.5, 1.0),
                                                           color=sns.color_palette()[0:2],
                                                           xlim=(-0.5, 32.5))
    dset[[texRename('sigma'), texRename('sigma2')]].plot.hist(
        ax=axes[3], bins=40, color=sns.color_palette()[0:2])

    # Set all the x-labels based on which histogram is displayed
    axes[0].set_xlabel(r'$K_x$')
    axes[1].set_xlabel(r'Conversion Factors')
    axes[2].set_xlabel(r'Effective Avidities ($f$)')
    axes[3].set_xlabel(r'Deviation Parameters ($\sigma^*$)')

    # Make x-axes appear logarithmic
    for ii in range(len(axes)):
        if ii != 2:
            axes[ii].set_xticklabels([eval("r'$10^{" + str(num) + "}$'")
                                      for num in axes[ii].get_xticks()])

    # Set all the x-limites based on which histogram is displayed
    axes[0].set_xlim(-13.0, axes[0].get_xlim()[1])
    axes[1].set_xlim(-6.0, axes[1].get_xlim()[1])
    axes[3].set_xlim(-1.5, axes[3].get_xlim()[1])

    axes[1].set_ylim(0, 5000)


def plotFit(fitMean, ax):
    ax.plot([0.01, 5], [0.01, 5], color='k', linestyle='-', linewidth=1)

    for _, row in fitMean.iterrows():
        colorr = FcgRidx[row['FcgR']]
        ax.errorbar(x=row['Fit'],
                    y=row['Meas_mean'],
                    yerr=row['Meas_std'],
                    marker=Igs[row['Ig']],
                    mfc=colorr,
                    mec=colorr,
                    ms=3,
                    mew=1.0,
                    ecolor=colorr,
                    linestyle='None')

    ax.set_ylabel('Fitted Prediction')
    ax.set_xlabel('Measured Ligand Binding')
    ax.loglog()
    ax.set_ylim(0.01, 5)
    ax.set_xlim(0.01, 5)


def GewekeDiagPlot(M, dset, ax):
    """ Get pvalues from geweke diagnostic from the dataset """
    from statsmodels.sandbox.stats.multicomp import multipletests
    from ..StoneHelper import geweke_chains

    _, pvalues = geweke_chains(dset)

    ptable = pd.DataFrame(pvalues, columns=FcgRlistL + texRenameList(M.pNames[8:]))
    ptable = pd.melt(ptable, var_name="param")

    ptable['PassFail'], ptable['cpval'], _, _ = multipletests(ptable.value, method='bonferroni')
    ptable['nlog'] = -np.log10(ptable.cpval)

    sns.stripplot(x='param',
                  y='nlog',
                  hue='PassFail',
                  ax=ax,
                  data=ptable)

    ax.set_ylabel(r'$-\log_{10}$(q-value)')
    ax.set_xlabel('')

    ax.set_xticklabels(ax.get_xticklabels(),
                       rotation=40,
                       rotation_mode="anchor",
                       ha="right",
                       fontsize=5,
                       position=(0, 0.075))

    # Remove legend created by sns.stripplot
    ax.get_legend().set_visible(False)


def AverageAvidity(ax):
    """ Produce the average of avidity of binding in the dilute case. """

    from ..StoneModel import StoneMod
    from ..StoneHelper import getMedianKx
    from itertools import product

    logRs = np.arange(3, 7, dtype=np.float)
    L0, gnus = 1.0E-18, 4
    Kas = np.logspace(2, 9, 20)

    table = pd.DataFrame(list(product(logRs, Kas)), columns=['logR', 'Ka'])

    def avAv(x):
        outt = StoneMod(x.logR, x.Ka, gnus, getMedianKx() * x.Ka, L0, fullOutput=True)

        return outt[1] / outt[0]

    table['AvAv'] = table.apply(avAv, axis=1)

    col = sns.crayon_palette(['Tickle Me Pink', 'Orange', 'Forest Green',
                              'Royal Purple'])
    sns.FacetGrid(hue='logR', data=table, palette=col).map(ax.plot, 'Ka', 'AvAv')

    ax.set_xscale('log')
    ax.set_ylabel('Average Binding Avidity')
    ax.set_xlabel(r'$K_a$')

    # Create the legend patches
    legend_patches = [matplotlib.patches.Patch(color=C, label=L) for
                      C, L in zip(col,
                                  [r'$10^{' + str(int(logr)) + '}$' for logr in logRs])]

    # Plot the legend
    ax.legend(handles=legend_patches, title=r'# Receptors', labelspacing=0.25)
