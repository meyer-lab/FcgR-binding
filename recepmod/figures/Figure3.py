from matplotlib import gridspec
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ..StoneModel import StoneMod
from ..StoneHelper import read_chain
from .FigureCommon import subplotLabel
import seaborn as sns
import string
import os
from itertools import product
from ..StoneTwoRecep import StoneTwo, StoneVgrid
from cycler import cycler

# Figure 3: Specific predictions regarding the coordinate effects of immune
# complex parameters.

def makeFigure():
    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Retrieve model and fit from hdf5 file
    M, dset = read_chain(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_chain.h5"))

    # Only keep good samples
    dsetFilter = dset.loc[dset['LL'] > (np.max(dset['LL'] - 4)),:]

    # Only keep Kx parameters
    dsetFilter = dsetFilter[['Kx1', 'Kdxa']].sample(n = 1000)

    # Setup plotting space
    f = plt.figure(figsize=(7,5))

    # Make grid
    gs1 = gridspec.GridSpec(2,3)

    # Get list of axis objects
    ax = [ f.add_subplot(gs1[x]) for x in range(6) ]

    # Plot subplot A
    PredictionVersusAvidity(dsetFilter, ax[0:4])

    # Plot from two receptor model
    TwoRecep(dset, ax = ax[4:6])

    for ii in range(len(ax)):
        subplotLabel(ax[ii], string.ascii_uppercase[ii])

    return f

# A) Predicted binding v conc of IC for varying avidity. B) Predicted
# multimerized FcgR v conc of IC for varying avidity. C) # of xlinks v conc of IC for varying avidity.
# D) The amount of binding versus number of crosslinks for two
# different affinities, with varied avidities.
def PredictionVersusAvidity(dset, ax):
    # Receptor expression
    Rexp = 3.0
    avidity = [1, 2, 4, 8, 16, 32]
    Ka = 1.0E5
    Kx = np.power(10, -6.7)
    ligand = np.logspace(start = -9, stop = -5, num = 40)

    current_palette = sns.color_palette()
    ax[1].set_prop_cycle(cycler('color', current_palette[1:]))
    ax[2].set_prop_cycle(cycler('color', current_palette[1:]))
    ax[3].set_prop_cycle(cycler('color', current_palette[1:]))

    def calculate(x):
        a = StoneMod(Rexp,Ka,x['avidity'],Kx,x['ligand'], fullOutput = True)

        return pd.Series(dict(bound = a[0], avidity = x['avidity'], ligand = x['ligand'], Rmulti = a[2], nXlink = a[3]))

    inputs = pd.DataFrame(list(product(avidity, ligand)), columns=['avidity', 'ligand'])

    outputs = inputs.apply(calculate, axis = 1)

    for ii in avidity:
        outputs[outputs['avidity'] == ii].plot(x = "ligand", y = "bound", ax = ax[0], logx = True)

        if ii > 1:
            outputs[outputs['avidity'] == ii].plot(x = "ligand", y = "Rmulti", ax = ax[1], logx = True)
            outputs[outputs['avidity'] == ii].plot(x = "ligand", y = "nXlink", ax = ax[2], logx = True)
            outputs[outputs['avidity'] == ii].plot(x = "bound", y = "nXlink", ax = ax[3], loglog = True)


# E) The predicted amount of multimerized receptor versus avidity for a cell
# expressing RIII and RIIB simultaneously. F) The predicted ratio (E)
# TODO: Examine distribution of receptor bound numbers over avidity
def TwoRecep(dset, ax = None):
    # Active, inhibitory
    Rexp = [3.0, 4.0]
    Ka = [2.0E6, 1.2E5]
    Kx = np.power(10, -6.7)
    avidity = [2, 4, 8, 16, 32]
    ligand = np.logspace(start = -12, stop = -5, num = 20)

    current_palette = sns.color_palette()
    ax[0].set_prop_cycle(cycler('color', current_palette[1:]))
    ax[1].set_prop_cycle(cycler('color', current_palette[1:]))

    def calculate(x):
        acl = StoneTwo(Rexp, Ka, Kx)

        oo = acl.getRmultiAll(int(x['avidity']), x['ligand'])

        return pd.Series(dict(ratio = oo[0]*oo[0]/(oo[0] + oo[1]), RmultiOne = oo[0], RmultiTwo = oo[1], ligand = x['ligand'], avidity = x['avidity']))


    inputs = pd.DataFrame(list(product(avidity, ligand)), columns=['avidity', 'ligand'])

    outputs = inputs.apply(calculate, axis = 1)

    for ii in avidity:
        outputs[outputs['avidity'] == ii].plot(x = "RmultiTwo", y = "RmultiOne", ax = ax[0], loglog = True)
        outputs[outputs['avidity'] == ii].plot(x = "ligand", y = "ratio", ax = ax[1], logx = True)

    #ax[1].set_ylim(0, 1000)


def Kdplot(dset, ax = None):
    # If no axis was provided make our own
    if ax == None:
        ax = plt.gca()

    Ka = 1.0E6

    def calculate(x):
        a = x['Kx1'] * Ka / (Ka + x['Kdxa'])

        return pd.Series(dict(Kx = a, Kx1 = x['Kx1'], Kdxa = x['Kdxa']))

    dset = dset.apply(calculate, axis = 1)

    dset.hist(column = "Kx", ax = ax, bins = 50)


def runTwoRecepPredict(ax):
    # Active, inhibitory
    Req = [1.0E4, 0]
    Kx = np.power(10, -6.7)

    # Ka
    Ka = [2.0E6, 1.2E5]
    L0 = 1E-4


    output = np.zeros((30,1), dtype = np.float64)

    def process(gnu):
        multGrid = np.zeros((gnu+1, gnu+1), dtype = np.float64)

        for ii in range(gnu+1):
            for jj in range(gnu+1):
                if ii > jj:
                    multGrid[ii,jj] = ii-jj-1

        gridd = StoneVgrid(Req,Ka,gnu,Kx,L0)

        gridd = gridd / np.sum(np.sum(gridd))

        gridd = np.multiply(gridd, multGrid)

        return np.sum(np.sum(gridd))

    for ii in range(2, 30):
        output[ii] = process(ii)



    ax.plot(output)
