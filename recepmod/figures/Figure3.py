"""
This creates Figure 3 which plots some predictions from the binding model.
"""

import matplotlib
matplotlib.use('AGG')
from itertools import product
import numpy as np
import pandas as pd
import seaborn as sns
from ..StoneModel import StoneMod
from ..StoneNRecep import StoneN
from ..StoneHelper import getMedianKx

# Specific predictions regarding the coordinate effects of immune complex parameters.

subsplits = 15

def makeFigure():
    import string

    from .FigureCommon import subplotLabel, getSetup

    # Get list of axis objects
    ax, f = getSetup((9, 5), (2, 4))

    # Plot subplot A
    PredictionVersusAvidity(ax[0:4])

    # Plot from two receptor model
    TwoRecep(ax=ax[4:6])

    # Plot of activity index versus Ka ratio
    varyAffinity(ax=ax[6])

    # Plot to show that highest affinity activating receptor is most sensitive to adjustment
    maxAffinity(ax=ax[7])

    for ii, item in enumerate(ax):
        subplotLabel(item, string.ascii_uppercase[ii])

    ax[0].legend([r'$\nu='+str(x)+r'$' for x in np.logspace(0, 5, 6, base=2, dtype=np.int).tolist()],
                 loc=1,
                 bbox_to_anchor=(0.5, 1))

    # Tweak layout
    f.tight_layout()

    return f


def plotRanges():
    avidity = np.logspace(0, 5, 6, base=2, dtype=np.int)
    ligand = np.logspace(start=-12, stop=-5, num=subsplits)
    Ka = [1.2E6, 1.2E5] # FcgRIIIA-Phe - IgG1, FcgRIIB - IgG1
    logR = [4.0, 4.5]

    return (ligand, avidity, Ka, logR)


def skipColor(ax):
    from cycler import cycler

    ax.set_prop_cycle(cycler('color', sns.color_palette()[1:]))


def PredictionVersusAvidity(ax):
    '''
    A) Predicted binding v conc of IC for varying avidity.
    B) Predicted multimerized FcgR v conc of IC for varying avidity.
    C) # of xlinks v conc of IC for varying avidity.
    D) Binding v # xlinks for two different affinities, with varied avidities.
    '''
    # Receptor expression
    ligand, avidity, Ka, logR = plotRanges()

    skipColor(ax[1])
    skipColor(ax[2])
    skipColor(ax[3])

    def calculate(x):
        a = StoneMod(logR[0],Ka[0],x['avidity'],getMedianKx()*Ka[0],x['ligand'], fullOutput=True)

        return pd.Series(dict(bound = a[0],
                              avidity = x['avidity'],
                              ligand = x['ligand'],
                              ligandEff = x['ligand'] * x['avidity'],
                              Rmulti = a[2],
                              nXlink = a[3]))

    inputs = pd.DataFrame(list(product(avidity, ligand)), columns=['avidity', 'ligand'])

    outputs = inputs.apply(calculate, axis = 1)

    for ii in avidity:
        curDat = outputs[outputs['avidity'] == ii]

        curDat.plot(x="ligand", y="bound", ax=ax[0], logx=True, legend=False)

        if ii > 1:
            curDat.plot(x="ligand", y="Rmulti", ax=ax[1], logx=True, legend=False)
            curDat.plot(x="ligand", y="nXlink", ax=ax[2], logx=True, legend=False)
            curDat.plot(x="bound", y="nXlink", ax=ax[3], loglog=True, legend=False)

    ax[0].set_xlabel('IC Concentration (M)')
    ax[1].set_xlabel('IC Concentration (M)')
    ax[2].set_xlabel('IC Concentration (M)')
    ax[0].set_ylabel(r'Bound Fc$\gamma$RIIIA-F')
    ax[1].set_ylabel(r'Multimerized Fc$\gamma$RIIIA-F')
    ax[2].set_ylabel(r'Fc$\gamma$RIIIA-F Nxlinks')
    ax[3].set_xlabel(r'Bound Fc$\gamma$RIIIA-F')
    ax[3].set_ylabel(r'Fc$\gamma$RIIIA-F Nxlinks')
    ax[3].set_ylim(1, 1E3)
    ax[3].set_xlim(1, 1E4)

def TwoRecep(ax):
    """
    E) Predicted multimerized receptor versus avidity for RIII-Phe + RIIB
    F) The predicted ratio (E)
    """
    if len(ax) != 2:
        raise ValueError("TwoRecep requires two axes to work on.")

    ligand, avidity, Ka, logR = plotRanges()

    skipColor(ax[0])
    skipColor(ax[1])

    def appFunc(x):
        model = StoneN(logR, Ka, getMedianKx(), x.avidity, x.ligand)

        rmulti = model.getRmultiAll()

        x['RmultiOne'] = rmulti[0]
        x['RmultiTwo'] = rmulti[1]
        x['activity'] = model.getActivity([1, -1])

        return x

    table = pd.DataFrame(list(product(avidity, ligand)), columns=['avidity', 'ligand'])

    table = table.apply(appFunc, axis=1)

    for ii in avidity[1::]:
        table[table['avidity'] == ii].plot(x="RmultiOne", y="RmultiTwo", ax=ax[0], legend=False)
        table[table['avidity'] == ii].plot(x="ligand", y="activity", ax=ax[1], logx=True, legend=False)

    ax[0].set_xlabel(r'Multimerized Fc$\gamma$RIIIA-F')
    ax[0].set_ylabel(r'Multimerized Fc$\gamma$RIIB')
    ax[1].set_xlabel('IC Concentration (M)')
    ax[1].set_ylabel('Activity Index')
    ax[0].set_ylim(0, 1E3)
    ax[0].set_xlim(0, 1E3)

def varyAffinity(ax):
    """
    Figure where affinity of the activating or inhibitory receptor varies.
    """
    _, avidities, Ka, logR = plotRanges()
    L0 = 1E-9

    skipColor(ax)

    affinities = Ka[0] * np.logspace(start=0, stop=2, num=subsplits)

    table = pd.DataFrame(list(product(affinities, avidities)), columns=['affinity', 'avidity'])

    def appFunc(x, ii):
        KaCur = Ka.copy()
        KaCur[ii] = x.affinity

        x['activity'] = StoneN(logR, KaCur, getMedianKx(), x.avidity, L0).getActivity([1, -1])
        x['ratio'] = KaCur[0] / KaCur[1]

        return x

    table = table.apply(lambda x: appFunc(x, 0), axis=1)

    for ii in avidities[1::]:
        table[table['avidity'] == ii].plot(ax=ax, x='ratio', y='activity', legend=False, loglog=True)

    ax.set_xlabel('$K_A$ Ratio (Activating/Inhibitory)')
    ax.set_ylabel('Activity Index')


def maxAffinity(ax):
    """ """
    from ..StoneModMouse import StoneModelMouse

    M = StoneModelMouse()

    Kas = np.squeeze(M.kaMouse[:, 2])

    logR = [4.0, 4.5, 4.0, 4.0]
    L0, gnu = 1.0E-9, 5

    table = pd.DataFrame(list(product(np.logspace(start=4, stop=9, num=subsplits), [0, 2, 3])),
                         columns=['adjust', 'ridx'])

    colors = sns.color_palette()

    def appFunc(x):
        KaCur = Kas.copy()
        KaCur[int(x.ridx)] = x.adjust

        x['activity'] = StoneN(logR, KaCur, getMedianKx(), gnu, L0).getActivity([1, -1, 1, 1])

        return x

    table = table.apply(appFunc, axis=1)

    sns.FacetGrid(hue='ridx', data=table).map(ax.loglog, 'adjust', 'activity')

    ax.loglog(M.kaMouse[0, 2], 512, color=colors[0], marker='o')
    ax.loglog(M.kaMouse[2, 2], 512, color=colors[1], marker='o')
    ax.loglog(M.kaMouse[3, 2], 512, color=colors[2], marker='o')

    ax.set_xlabel(r'$K_A$ of Fc$\gamma$R Adjusted')
    ax.set_ylabel('Activity Index')
    ax.set_xlim(1.0E4, 1.0E9)

    patchA = matplotlib.patches.Patch(color=colors[0], label=r'Fc$\gamma$RI')
    patchB = matplotlib.patches.Patch(color=colors[1], label=r'Fc$\gamma$RIII')
    patchC = matplotlib.patches.Patch(color=colors[2], label=r'Fc$\gamma$RIV')
    ax.legend(handles=[patchA, patchB, patchC])
