import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Figure 5: Predict in vivo response

def makeFigure():
    print("Starting Figure 5")

    import string
    import os
    from matplotlib import gridspec
    from ..StoneHelper import getMedianKx
    from .FigureCommon import subplotLabel

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # We're going to need Kx
    Kx = getMedianKx()

    # Setup plotting space
    f = plt.figure(figsize=(7,5))

    # Make grid
    gs1 = gridspec.GridSpec(2,3)

    # Get list of axis objects
    ax = [ f.add_subplot(gs1[x]) for x in range(6) ]

    # Make binding data PCA plot
    ClassAvidityPCA(ax=ax[1])

    # Show performance of in vivo regression model
    InVivoPredictVsActual(ax=ax[4])

    for ii, item in enumerate(ax):
        subplotLabel(item, string.ascii_uppercase[ii])

    # Tweak layout
    plt.tight_layout()

    return f


def ClassAvidityPCA(ax=None):
    """ Plot the generated binding data for different classes and avidities in PCA space. """

    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()






def InVivoPredictVsActual(ax=None):
    """ Plot predicted vs actual for regression of conditions in vivo. """

    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()


def InVivoPredictVsActualAffinities(ax=None):
    """ Plot predicted vs actual for regression of conditions in vivo using affinity. """

    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()
