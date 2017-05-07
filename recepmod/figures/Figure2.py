import string
import numpy as np
import seaborn as sns
from matplotlib import rcParams
from ..StoneHelper import read_chain, getFitMeasMergedSummarized, geweke_chains
from .FigureCommon import Igs, FcgRidx, subplotLabel, texRename, texRenameList, getSetup, Legend, FcgRidxL


def makeFigure():
    # Retrieve model and fit from hdf5 file
    M, dset = read_chain()

    pBest = dset.iloc[np.argmax(dset['LL']), :][2:].as_matrix()
    
    rcParams['lines.markeredgewidth'] = 1.0

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

    ax.set_ylabel(r'$\log_{10}$(Fc$\gamma$R Expression)')

def histSubplots(dset, axes):
    dset.columns = texRenameList(dset.columns)

    dset[[texRename('Kx1')]].plot.hist(ax=axes[0], bins = 20, color=sns.color_palette()[0])
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
    axes[3].set_xlabel(r'Deviation Parameter ($\sigma$)')

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
                    ecolor=colorr,
                    linestyle='None')

    ax.set_ylabel('Fitted prediction')
    ax.set_xlabel('Measured ligand binding')
    ax.loglog()
    ax.set_ylim(0.01, 5)
    ax.set_xlim(0.01, 5)

def GewekeDiagPlot(M,dset,ax):
    # Get pvalues from geweke diagnostic from the dataset
    _, pvalues = geweke_chains(dset)
    # Get number of walkers from pvalues
    nwalkers = len(pvalues)
    # Plot horizontal red line to discriminate between acceptable (<=0.05) and
    # unacceptable (>0.05) pvalues from Geweke diagnostic
    ax.plot([j-1 for j in range(M.Nparams+2)],[0.05]*(M.Nparams+2),'r-')

    # Transpose pvalues from an array of shape 52, 13 to one of shape
    # 13, 52, while taking the negative logarithms of the pvalues
    pvalues = (-np.log(np.array(pvalues))).T.tolist()

    # Plot green Xs per walker per parameter
    for j in range(M.Nparams):
        for pval in pvalues[j]:
            if pval > -np.log(0.05):
                x = 'kx'
            else:
                x = 'gx'
            ax.plot([j],[pval],x)
        
    ax.set_xbound(-1,M.Nparams)
    ax.set_xticks([j for j in range(M.Nparams)])
    ax.set_xticklabels(list(FcgRidx)+texRenameList(M.pNames[6:-1]),rotation=40)
    ax.set_ylabel(r'$-\log$(p-values)')
    ax.xaxis.grid(False)
    leg = ax.legend((r'$p=0.05$','pass','fail'),framealpha=0.0)
