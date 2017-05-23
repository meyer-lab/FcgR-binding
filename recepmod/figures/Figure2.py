"""
This creates Figure 2 which fits the binding data to a model.
"""

import string
import numpy as np
import pandas as pd
import seaborn as sns
from ..StoneHelper import read_chain, getFitMeasMergedSummarized, geweke_chains
from .FigureCommon import Igs, FcgRidx, subplotLabel, texRename, texRenameList, getSetup, Legend, FcgRidxL, getRquant


def makeFigure():
    # Retrieve model and fit from hdf5 file
    M, dset = read_chain()

    pBest = dset.iloc[np.argmax(dset['LL']), :][2:].as_matrix()

    # Get list of axis objects
    ax, f = getSetup((7, 6), (3, 3))

    # Blank out for the cartoon
    ax[0].axis('off')
    ax[1].axis('off')

    ax[1].legend(handles=Legend(FcgRidxL, Igs))

    # Show predicted versus actual
    plotFit(getFitMeasMergedSummarized(M, pBest), ax=ax[2])

    # Make Geweke diagnostic subplot
    GewekeDiagPlot(M, dset, ax[3])

    # Make histogram subplots
    histSubplots(dset, axes=ax[4:8])

    # Make receptor expression subplot
    violinPlot(dset, ax=ax[8])

    subplotLabel(ax[0], 'A')

    for ii, item in enumerate(ax[2:9]):
        subplotLabel(item, string.ascii_uppercase[ii+1])

    # Try and fix overlapping elements
    f.tight_layout()

    return f


def violinPlot(dset, ax):
    dset = dset[['Rexp']]
    dset.columns = FcgRidxL.keys()

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
        ax.plot([ii]*len(row), row, 'k_', mew=1.0)

    ax.set_ylim(5, 7)

def histSubplots(dset, axes):
    dset.columns = texRenameList(dset.columns)

    dset[[texRename('Kx1')]].plot.hist(ax=axes[0], bins = 20, color=sns.color_palette()[0], legend=False)
    dset[[texRename('sigConv1'), texRename('sigConv2')]].plot.hist(ax=axes[1], bins = 20, color=sns.color_palette()[0:2])
    dset[[texRename('gnu1'), texRename('gnu2')]].plot.hist(ax=axes[2],
                                           bins = np.arange(-0.5, 32.5, 1.0),
                                           color=sns.color_palette()[0:2],
                                           xlim = (-0.5, 32.5))
    dset[[texRename('sigma'), texRename('sigma2')]].plot.hist(ax=axes[3], bins = 40, color=sns.color_palette()[0:2])

    # Set all the x-labels based on which histogram is displayed
    axes[0].set_xlabel(r'$\log_{10}$(K$_x$)')
    axes[1].set_xlabel(r'$\log_{10}$(Conversion Factor)')
    axes[2].set_xlabel(r'Effective Avidity ($\nu$)')
    axes[3].set_xlabel(r'$\log_{10}$[Deviation Parameter ($\sigma$)]')

    # Set all the x-limites based on which histogram is displayed
    axes[0].set_xlim(-13.0,axes[0].get_xlim()[1])
    axes[1].set_xlim(-6.0,axes[1].get_xlim()[1])
    axes[3].set_xlim(-1.5,axes[3].get_xlim()[1])

    axes[1].set_ylim(0, 5000)

    print(np.mean(np.power(10, dset[texRename('sigConv2')] - dset[texRename('sigConv1')])))

    print(np.power(10, np.std(dset[texRename('sigma2')])))


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

    ax.set_ylabel('Fitted prediction')
    ax.set_xlabel('Measured ligand binding')
    ax.loglog()
    ax.set_ylim(0.01, 5)
    ax.set_xlim(0.01, 5)

def GewekeDiagPlot(M,dset,ax):
    # Get pvalues from geweke diagnostic from the dataset
    from statsmodels.sandbox.stats.multicomp import multipletests

    _, pvalues = geweke_chains(dset)

    ptable = pd.DataFrame(pvalues, columns=list(FcgRidxL)+texRenameList(M.pNames[8:]))
    ptable = pd.melt(ptable, var_name="param")

    ptable['PassFail'], ptable['cpval'], _, _ = multipletests(ptable.value, method='bonferroni')
    ptable['nlog'] = -np.log10(ptable.cpval)

    sns.stripplot(x='param',
                  y='nlog',
                  hue='PassFail',
                  ax=ax,
                  data=ptable)

    ax.set_ylabel('-log10(q-value)')
    ax.set_xlabel('')

    ax.set_xticklabels(ax.get_xticklabels(),
                       rotation=40,
                       rotation_mode="anchor",
                       ha="right",
                       fontsize=5,
                       position=(0,0.075))

    print('YAAAAAAAAAAAAAAAS')
    print(ax.get_xticklabels()[0].get_position())


def AverageAvidity():
    """ Produce the average of avidity of binding in the dilute case. """

    from ..StoneModel import StoneMod
    from ..StoneHelper import getMedianKx
    from itertools import product

    KxIn = getMedianKx()

    logRs = np.linspace(2, 5, 4, dtype=np.float)
    L0 = 1.0E-12
    gnus = np.arange(1, 11)
    Kas = np.logspace(2, 8, 4, dtype=np.float)

    table = pd.DataFrame(list(product(gnus, logRs, Kas)), columns=['gnu', 'logR', 'Ka'])

    def avAv(x):
        outt = StoneMod(x.logR, x.Ka, x.gnu, KxIn*x.Ka, L0, fullOutput=True)

        x['AvAv'] = outt[1] / outt[0]

        return x

    table = table.apply(avAv, axis=1)

    return table
