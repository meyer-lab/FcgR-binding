import os
from matplotlib import gridspec
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from .FigureCommon import FcgRidx, subplotLabel

def makeFigure():
    from ..StoneHelper import read_chain, mapMCMC, getFitPrediction

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Retrieve model and fit from hdf5 file
    M, dset = read_chain(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_chain.h5"))

    # Filter for only remotely likely parameter sets
    dset = dset.loc[dset['LL'] > np.min(dset['LL']) - 3,:]

    dsetSamp = dset.sample(200)

    runFunc = lambda x: getFitPrediction(M, x[2:])

    output = mapMCMC(runFunc, dsetSamp)

    # Setup plotting space
    f = plt.figure(figsize=(7, 6))

    # Make grid
    gs1 = gridspec.GridSpec(4, 3)

    # Get list of axis objects
    ax = [ f.add_subplot(gs1[x]) for x in range(0,12) ]

    subplotLabel(ax[0], 'A')
    subplotLabel(ax[6], 'B')

    # Bound / total receptor prediction
    Rbndplot(output.copy(), axarr = ax[0:])

    # Multimerized receptor prediction
    Rmultiplot(output.copy(), axarr = ax[6:])

    # Tweak layout
    plt.tight_layout()

    return f

def Rbndplot(output, axarr = None):
    output['RbndPred'] = output.apply(lambda row: (row['RbndPred'] / (row['RbndPred'] + row['Req'])), axis=1)

    if axarr is None:
        f = plt.figure()

        # Make grid
        gs1 = gridspec.GridSpec(2,3)

        # Create 6 axes for each FcgR
        axarr = [ f.add_subplot(gs1[x]) for x in range(6) ]

    fcIter = zip(axarr, FcgRidx.keys())

    # Loop through receptors creating plot
    for axx, fcr in fcIter:
        sns.boxplot(x="Ig",
                    y = 'RbndPred',
                    hue="TNP",
                    data=output.loc[output['FcgR'] == fcr,:],
                    ax = axx,
                    showfliers=False)

        axx.set_ylabel(r'Fc$\gamma$R bound/total')
        axx.set_xlabel("")
        axx.set_ylim((0, 1))
        axx.legend_.remove()
        axx.set_title(fcr)

def Rmultiplot(output, axarr = None):
    output['RmultiPred'] = output.groupby(['pSetNum'])['RmultiPred'].apply(lambda x: x / x.mean())
    output['nXlinkPred'] = output.groupby(['pSetNum'])['nXlinkPred'].apply(lambda x: x / x.mean())

    if axarr is None:
        f = plt.figure()

        # Make grid
        gs1 = gridspec.GridSpec(2,3)

        # Create 6 axes for each FcgR
        axarr = [ f.add_subplot(gs1[x]) for x in range(6) ]

    fcIter = zip(axarr, FcgRidx.keys())

    # Loop through receptors creating plot
    for axx, fcr in fcIter:
        sns.boxplot(x="Ig",
                    y = "nXlinkPred",
                    hue="TNP",
                    data=output.loc[output['FcgR'] == fcr,:],
                    ax = axx)

        axx.set_ylabel(r'Multimerized Fc$\gamma$R')
        axx.set_xlabel("")
        #axx.set_ylim((0, 4))
        axx.legend_.remove()
        axx.set_title(fcr)
