import os
import string
from matplotlib import gridspec, rcParams
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from .FigureCommon import Igs, FcgRidx, makeFcIgLegend, subplotLabel

def makeFigure():
    from ..StoneHelper import read_chain

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Retrieve model and fit from hdf5 file
    M, dset = read_chain(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_chain.h5"))

    # Filter for only remotely likely parameter sets
    dset = dset.loc[dset['LL'] > np.min(dset['LL']) - 3,:]

    # Setup plotting space
    f = plt.figure(figsize=(7,6))

    # Make grid
    gs1 = gridspec.GridSpec(3,3)

    # Get list of axis objects
    ax = [ f.add_subplot(gs1[x]) for x in range(1,9) ]

    #
    plotFitBinding(M, dset, quant = "LbndPred", axarr = ax)

    return f

def plotFitBinding(M, dset, quant = "LbndPred", axarr = None):
    from ..StoneHelper import mapMCMC, getFitPrediction, reduceMCMC

    dsetSamp = dset.sample(1000)

    runFunc = lambda x: getFitPrediction(M, x[2:])

    output = mapMCMC(runFunc, dsetSamp)

    output[quant] = output.groupby(['pSetNum'])[quant].apply(lambda x: x / x.mean())

    if axarr is None:
        f = plt.figure()

        # Make grid
        gs1 = gridspec.GridSpec(2,3)

        # Create 6 axes for each FcgR
        axarr = [ f.add_subplot(gs1[x]) for x in range(6) ]

        built = True
    else:
        built = False

    fcIter = zip(axarr, FcgRidx.keys())

    # Loop through receptors creating plot
    for axx, fcr in fcIter:
        sns.boxplot(x="Ig",
                    y = quant,
                    hue="TNP",
                    data=output.loc[output['FcgR'] == fcr,:],
                    ax = axx,
                    showfliers=False)

        axx.set_ylabel("Binding (RU)")
        axx.set_xlabel("")
        axx.set_ylim((0, np.nanmax(output.loc[output['FcgR'] == fcr,quant].as_matrix())*1.05))
        axx.legend_.remove()
        axx.set_title(fcr)

    if built is True:
        plt.tight_layout()
