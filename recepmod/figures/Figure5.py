import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from ..StoneModMouse import StoneModelMouse

# Figure 5: Predict in vivo response

def makeFigure():
    print("Starting Figure 5")

    import string
    from matplotlib import gridspec
    from ..StoneHelper import getMedianKx
    from .FigureCommon import subplotLabel

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # We're going to need Kx
    Kx = getMedianKx()

    # Setup plotting space
    f = plt.figure(figsize=(7,5))

    # Make grid
    gs1 = gridspec.GridSpec(3,3)

    # Get list of axis objects
    ax = [ f.add_subplot(gs1[x]) for x in range(9) ]

    # Blank out for the cartoon
    ax[0].axis('off')

    # Make binding data PCA plot
    ClassAvidityPCA(ax=ax[1])

    # Show performance of in vivo regression model
    InVivoPredictVsActual(ax=ax[2])

    # Show model components
    InVivoPredictComponents(ax=ax[3])

    # Leave components out plot
    RequiredComponents(ax=ax[4])

    # Show performance of affinity prediction
    InVivoPredictVsActualAffinities(ax=ax[5])

    # Predict class/avidity effect
    ClassAvidityPredict(ax=ax[6])

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


    ax.set_ylabel('PC 2')
    ax.set_xlabel('PC 1')

def InVivoPredictVsActual(ax=None):
    """ Plot predicted vs actual for regression of conditions in vivo. """

    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()


    ax.set_ylabel('Predicted Effect')
    ax.set_xlabel('Actual Effect')

def InVivoPredictComponents(ax=None):
    """ Plot model components. """

    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()

    logR = np.log10(10**5)
    z = [logR, logR, logR, logR, logR, logR, 10**(-12.25), 10]

    M = StoneModelMouse()
    model = M.NimmerjahnKnockdownLasso(z)




    ax.set_ylabel('Weightings')
    ax.set_xlabel('Components')

def RequiredComponents(ax=None):
    """ Plot model components. """

    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()


    ax.set_ylabel('Leave One Intervention Out Perc Explained')
    ax.set_xlabel('Components')

def InVivoPredictVsActualAffinities(ax=None):
    """ Plot predicted vs actual for regression of conditions in vivo using affinity. """

    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()

    Mod = StoneModelMouse()

    _, _, data = Mod.NimmerjahnPredictByAffinities()

    data.plot(kind='scatter', x='Effectiveness', y='CrossPredict', ax=ax)
    ax.set_ylabel('Predicted Effect')
    ax.set_xlabel('Actual Effect')

def ClassAvidityPredict(ax=None):
    """ Plot prediction of in vivo model with varying avidity and class. """
    from ..StoneModMouse import MultiAvidityPredict, StoneModelMouse

    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()

    logR = np.log10(10**5)
    z = [logR, logR, logR, logR, logR, logR, 10**(-12.25), 10]

    M = StoneModelMouse()
    model = M.NimmerjahnKnockdownLasso(z)

    z[7] = 30

    table = MultiAvidityPredict(M, z, np.insert(model.coef_, 0, model.intercept_))

    sns.factorplot(ax=ax, x='Avidity', y='Predict', hue='Ig', data=table, size=1)


    ax.set_ylabel('Predicted Effect')


