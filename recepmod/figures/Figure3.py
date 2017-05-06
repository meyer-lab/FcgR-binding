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

    # Tweak layout
    f.tight_layout()

    return f


def plotRanges():
    avidity = np.logspace(0, 5, 6, base=2, dtype=np.int)
    ligand = np.logspace(start=-12, stop=-5, num=50)
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
        a = StoneMod(logR[0],Ka[0],x['avidity'],getMedianKx()*Ka[0],x['ligand'], fullOutput = True)

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

    _, _, Ka, logR = plotRanges()

    gnu = 5
    L0 = 1E-9

    tableAct = pd.DataFrame(Ka[0] * np.logspace(start=0, stop=2, num=10), columns=['affinity'])

    def appFunc(x, ii):
        KaCur = Ka.copy()
        KaCur[ii] = x.affinity

        x['activity'] = StoneN(logR, KaCur, getMedianKx(), gnu, L0).getActivity([1, -1])
        x['ratio'] = KaCur[0] / KaCur[1]

        return x

    tableAct = tableAct.apply(lambda x: appFunc(x, 0), axis=1)

    tableAct.plot(ax=ax, x='ratio', y='activity', legend=False, loglog=True)

    ax.set_xlabel('Log Ka Ratio (Activating/Inhibitory)')
    ax.set_ylabel('Activity Index')

def maxAffinity(ax):
    """ """
    from ..StoneModMouse import StoneModelMouse

    M = StoneModelMouse()

    Kas = np.squeeze(M.kaMouse[:, 2])

    logR = [4.0, 4.5, 4.0, 4.0]
    L0, gnu = 1.0E-9, 5

    table = pd.DataFrame(np.logspace(start=-4, stop=4, num=20), columns=['adjust'])

    def appFunc(x, ii):
        KaCur = Kas.copy()
        KaCur[ii] *= x.adjust

        x['activity'] = StoneN(logR, KaCur, getMedianKx(), gnu, L0).getActivity([1, -1, 1, 1])
        x['KaCur'] = KaCur[ii]

        return x

    # TODO: Indicate where receptors are when not varied.

    tableA = table.apply(lambda x: appFunc(x, 0), axis=1)
    tableC = table.apply(lambda x: appFunc(x, 2), axis=1)
    tableD = table.apply(lambda x: appFunc(x, 3), axis=1)

    tableA.plot(ax=ax, x='KaCur', y='activity', legend=False, loglog=True)
    tableC.plot(ax=ax, x='KaCur', y='activity', legend=False, loglog=True)
    tableD.plot(ax=ax, x='KaCur', y='activity', legend=False, loglog=True)

    ax.plot(M.kaMouse[0, 2], 500, 'k.')
    ax.plot(M.kaMouse[1, 2], 500, 'k.')
    ax.plot(M.kaMouse[3, 2], 500, 'k.')

    ax.set_xlabel(r'Ka of Fc$\gamma$R Adjusted')
    ax.set_ylabel('Activity Index')

    ax.set_xlim(1.0E4, 1.0E9)
