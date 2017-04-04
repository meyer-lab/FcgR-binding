from itertools import product
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from cycler import cycler
from ..StoneModel import StoneMod
from ..StoneHelper import read_chain
from .FigureCommon import subplotLabel
from ..StoneTwoRecep import StoneTwo

# Figure 4: Specific predictions regarding the coordinate effects of immune
# complex parameters.

def makeFigure():
    print("Starting Figure 4")

    import string
    import os
    from matplotlib import gridspec

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Retrieve model and fit from hdf5 file
    _, dset = read_chain(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_chain.h5"))

    # Only keep good samples
    dsetFilter = dset.loc[dset['LL'] > (np.max(dset['LL'] - 4)),:]
    Kx = np.power(10, np.median(dsetFilter['Kx1']))

    # Setup plotting space
    f = plt.figure(figsize=(7,5))

    # Make grid
    gs1 = gridspec.GridSpec(2,3)

    # Get list of axis objects
    ax = [ f.add_subplot(gs1[x]) for x in range(6) ]

    # Plot subplot A
    PredictionVersusAvidity(ax[0:4], Kx)

    # Plot from two receptor model
    TwoRecep(Kx, ax = ax[4:6])

    for ii, item in enumerate(ax):
        subplotLabel(item, string.ascii_uppercase[ii])

    # Tweak layout
    plt.tight_layout()

    return f

def plotRanges():
    avidity = np.logspace(0, 5, 6, base = 2, dtype = np.int)
    ligand = np.logspace(start = -12, stop = -5, num = 40)
    Ka = [1.2E6, 1.2E5] # FcgRIIIA-Phe - IgG1, FcgRIIB - IgG1
    logR = [4.0, 4.5]

    return (ligand, avidity, Ka, logR)

def skipColor(ax):
    ax.set_prop_cycle(cycler('color', sns.color_palette()[1:]))

def PredictionVersusAvidity(ax, Kx):
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
        a = StoneMod(logR[0],Ka[0],x['avidity'],Kx*Ka[0],x['ligand'], fullOutput = True)

        return pd.Series(dict(bound = a[0],
                              avidity = x['avidity'],
                              ligand = x['ligand'],
                              Rmulti = a[2],
                              nXlink = a[3]))

    inputs = pd.DataFrame(list(product(avidity, ligand)), columns=['avidity', 'ligand'])

    outputs = inputs.apply(calculate, axis = 1)

    for ii in avidity:
        curDat = outputs[outputs['avidity'] == ii]

        curDat.plot(x = "ligand", y = "bound", ax = ax[0], logx = True, legend = False)

        if ii > 1:
            curDat.plot(x = "ligand", y = "Rmulti", ax = ax[1], logx = True, legend = False)
            curDat.plot(x = "ligand", y = "nXlink", ax = ax[2], logx = True, legend = False)
            curDat.plot(x = "bound", y = "nXlink", ax = ax[3], loglog = True, legend = False)

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

def TwoRecep(Kx, ax = None):
    """
    E) Predicted multimerized receptor versus avidity for RIII-Phe + RIIB
    F) The predicted ratio (E)
    """
    ligand, avidity, Ka, logR = plotRanges()

    skipColor(ax[0])
    skipColor(ax[1])

    acl = StoneTwo(logR, Ka, Kx)

    inputs = pd.DataFrame(list(product(avidity, ligand)), columns=['avidity', 'ligand'])

    outputs = inputs.apply(lambda x: acl.getAllProps(int(x['avidity']), x['ligand']), axis = 1)

    for ii in avidity[1::]:
        outputs[outputs['avidity'] == ii].plot(x = "RmultiOne", y = "RmultiTwo", ax = ax[0], legend = False)
        outputs[outputs['avidity'] == ii].plot(x = "ligand", y = "activity", ax = ax[1], logx = True, legend = False)

    ax[0].set_xlabel(r'Multimerized Fc$\gamma$RIIIA-F')
    ax[0].set_ylabel(r'Multimerized Fc$\gamma$RIIB')
    ax[1].set_xlabel('IC Concentration (M)')
    ax[1].set_ylabel('Activity Index')
    ax[0].set_ylim(0, 1E3)
    ax[0].set_xlim(0, 1E3)
