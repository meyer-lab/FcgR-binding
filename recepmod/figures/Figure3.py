"""
This creates Figure 3 which plots some predictions from the binding model.
"""

from itertools import product
import numpy as np
import pandas as pd
import seaborn as sns
from ..StoneModel import StoneMod
from ..StoneNRecep import StoneN
from ..StoneHelper import getMedianKx

# Specific predictions regarding the coordinate effects of immune complex parameters.

subsplits = 100


def makeFigure():
    import string
    from .FigureCommon import subplotLabel, getSetup

    # Get list of axis objects
    ax, f = getSetup((7, 6), (3, 3))

    # Plot subplot A
    # PredictionVersusAvidity(ax[0:4])

    # Plot from two receptor model
    # TwoRecep(ax=ax[5:7])

    # Plot of activity index versus Ka ratio
    # varyAffinity(ax=ax[7])

    # Plot to show that highest affinity activating receptor is most sensitive to adjustment
    maxAffinity(ax=ax[8])

    for ii, item in enumerate(ax):
        subplotLabel(item, string.ascii_uppercase[ii])

    avidities = np.logspace(0, 5, 6, base=2, dtype=np.int).tolist()
    ax[0].legend([r'$' + str(x) + r'$' for x in avidities],
                 loc=1,
                 bbox_to_anchor=(0.5, 1))

    # Remove center subplot for overlaid cartoon
    ax[4].set_axis_off()

    # Tweak layout
    f.tight_layout()

    return f


def plotRanges():
    avidity = np.logspace(0, 5, 6, base=2, dtype=np.int)
    ligand = np.logspace(start=-12, stop=-5, num=subsplits)
    Ka = [1.2E6, 1.2E5]  # FcgRIIIA-Phe - IgG1, FcgRIIB - IgG1
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
        a = StoneMod(logR[0], Ka[0], x['avidity'],
                     getMedianKx() * Ka[0], x['ligand'], fullOutput=True)

        return pd.Series(dict(bound=a[0],
                              avidity=x['avidity'],
                              ligand=x['ligand'],
                              ligandEff=x['ligand'] * x['avidity'],
                              Rmulti=a[2],
                              nXlink=a[3]))

    inputs = pd.DataFrame(list(product(avidity, ligand)), columns=['avidity', 'ligand'])

    outputs = inputs.apply(calculate, axis=1)

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
    ax[0].set_ylabel(r'Bound hFc$\gamma$RIIIA-F')
    ax[1].set_ylabel(r'Multimerized hFc$\gamma$RIIIA-F')
    ax[2].set_ylabel(r'hFc$\gamma$RIIIA-F Nxlinks')
    ax[3].set_xlabel(r'Bound hFc$\gamma$RIIIA-F')
    ax[3].set_ylabel(r'hFc$\gamma$RIIIA-F Nxlinks')
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

    colors = dict(zip(avidity[1::], sns.color_palette()[1::]))

    for ii in avidity[1::]:
        table[table['avidity'] == ii].plot(x="ligand",
                                           y="activity",
                                           ax=ax[1],
                                           logx=True,
                                           legend=False)
        x0 = table[table['avidity'] == ii]['RmultiOne'].values
        y0 = table[table['avidity'] == ii]['RmultiTwo'].values
        ax[0].plot(x0, y0)
        for x, y, xx, yy in zip(x0[0:-1:10], y0[0:-1:10],
                                (x0 - np.roll(x0, 1))[0:-1:10],
                                (y0 - np.roll(y0, 1))[0:-1:10]):
            ax[0].plot(x, y, marker=(3, 0, np.arctan2(yy, xx) / np.pi * 180 - 90),
                       color=colors[ii])
    ax[0].set_xlabel(r'Multimerized hFc$\gamma$RIIIA-F')
    ax[0].set_ylabel(r'Multimerized hFc$\gamma$RIIB')
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
        table[table['avidity'] == ii].plot(ax=ax, x='ratio', y='activity',
                                           legend=False)

    ax.set_xscale('log')
    ax.set_xlabel('$K_a$ Ratio (Activating/Inhibitory)')
    ax.set_ylabel('Activity Index')


def maxAffinity(ax):
    """ Show that the A/I ratio is consistent with activity quantity. """
    import matplotlib
    from ..StoneModMouse import StoneModelMouse

    Kas = np.squeeze(StoneModelMouse().kaMouse[:, 2])

    logR = [4.0, 4.5, 4.0, 4.0]
    L0, gnu = 1.0E-9, 5

    baselineAct = StoneN(logR, Kas, getMedianKx(), gnu, L0).getActivity([1, -1, 1, 1])

    table = pd.DataFrame(list(product(np.logspace(start=4, stop=9, num=subsplits), [0, 2, 3])),
                         columns=['adjust', 'ridx'])

    colors = sns.crayon_palette(['Brick Red', 'Forest Green', 'Brown'])

    def appFunc(x):
        KaCur = Kas.copy()
        KaCur[int(x.ridx)] = x.adjust

        x['activity'] = StoneN(logR, KaCur, getMedianKx(), gnu, L0).getActivity([1, -1, 1, 1])
        # Make ridx == 0 visible
        if x['ridx'] == 0:
            x['activity'] += 50

        return x

    table = table.apply(appFunc, axis=1)

    ax.plot(Kas[0], baselineAct + 50, color=colors[0], marker='o')

    sns.FacetGrid(hue='ridx', data=table, palette=colors).map(ax.plot, 'adjust', 'activity')

    ax.plot(Kas[2], baselineAct, color=colors[1], marker='o')
    ax.plot(Kas[3], baselineAct, color=colors[2], marker='o')

    ax.set_xlabel(r'$K_a$ of Adjusted mFc$\gamma$R')
    ax.set_ylabel('Activity Index')
    ax.set_xscale('log')
    ax.set_xlim(1.0E4, 1.0E9)

    patchA = matplotlib.patches.Patch(color=colors[0], label=r'mFc$\gamma$RI')
    patchB = matplotlib.patches.Patch(color=colors[1], label=r'mFc$\gamma$RIII')
    patchC = matplotlib.patches.Patch(color=colors[2], label=r'mFc$\gamma$RIV')
    ax.legend(handles=[patchA, patchB, patchC])
