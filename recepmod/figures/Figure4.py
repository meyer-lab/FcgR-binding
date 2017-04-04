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

# Figure 3: Specific predictions regarding the coordinate effects of immune
# complex parameters.

def makeFigure():
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

    return f

#
def PredictionVersusAvidity(ax, Kx):
    '''
    A) Predicted binding v conc of IC for varying avidity.
    B) Predicted multimerized FcgR v conc of IC for varying avidity.
    C) # of xlinks v conc of IC for varying avidity.
    D) Binding v # xlinks for two different affinities, with varied avidities.
    '''
    # Receptor expression
    Rexp = 4.0
    avidity = [1, 2, 8, 32, 128]
    Ka = 1.2E6 # FcgRIIIA-Phe - IgG1
    ligand = np.logspace(start = -12, stop = -5, num = 60)

    current_palette = sns.color_palette()
    ax[1].set_prop_cycle(cycler('color', current_palette[1:]))
    ax[2].set_prop_cycle(cycler('color', current_palette[1:]))
    ax[3].set_prop_cycle(cycler('color', current_palette[1:]))

    def calculate(x):
        a = StoneMod(Rexp,Ka,x['avidity'],Kx*Ka,x['ligand'], fullOutput = True)

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
    ax[0].set_xlabel(r'Bound Fc$\gamma$R')
    ax[1].set_xlabel(r'Multimerized Fc$\gamma$R')
    ax[2].set_xlabel(r'Fc$\gamma$R Nxlinks')


def TwoRecep(Kx, ax = None):
    """
    E) Predicted multimerized receptor versus avidity for RI + RIIB
    F) The predicted ratio (E)
    """
    # Active, inhibitory
    Ka = [6.5E7, 1.2E5]
    logR = [1.0, 4.5]
    avidity = [1, 2, 8, 32, 128]
    ligand = np.logspace(start = -12, stop = -5, num = 40)

    current_palette = sns.color_palette()
    ax[0].set_prop_cycle(cycler('color', current_palette[1:]))
    ax[1].set_prop_cycle(cycler('color', current_palette[1:]))

    acl = StoneTwo(logR, Ka, Kx)

    def calculate(x):
        return acl.getAllProps(int(x['avidity']), x['ligand'])

    inputs = pd.DataFrame(list(product(avidity, ligand)), columns=['avidity', 'ligand'])

    outputs = inputs.apply(calculate, axis = 1).assign(ratio = lambda x: x.RmultiOne / x.RmultiTwo)

    for ii in avidity:
        outputs[outputs['avidity'] == ii].plot(x = "RmultiTwo", y = "RmultiOne", ax = ax[0], loglog = True, legend = False)
        outputs[outputs['avidity'] == ii].plot(x = "ligand", y = "ratio", ax = ax[1], logx = True, legend = False)
