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

    # Load murine class
    Mod = StoneModelMouse()

    # Setup plotting space
    f = plt.figure(figsize=(7, 5))

    # Make grid
    gs1 = gridspec.GridSpec(3, 3)

    # Get list of axis objects
    ax = [ f.add_subplot(gs1[x]) for x in range(9) ]

    # Blank out for the cartoon
    ax[0].axis('off')

    # Make binding data PCA plot
    ClassAvidityPCA(Mod, ax=ax[1])

    # Show performance of in vivo regression model
    InVivoPredictVsActual(Mod, ax=ax[2])

    # Show model components
    InVivoPredictComponents(Mod, ax=ax[3])

    # Leave components out plot
    RequiredComponents(ax=ax[4])

    # Show performance of affinity prediction
    InVivoPredictVsActualAffinities(Mod, ax=ax[5])

    # Predict class/avidity effect
    ClassAvidityPredict(Mod, ax=ax[6])

    for ii, item in enumerate(ax):
        subplotLabel(item, string.ascii_uppercase[ii])

    # Tweak layout
    plt.tight_layout()

    return f

Igs = {'IgG1', 'IgG2a', 'IgG2b', 'IgG3'}
Igidx = dict(zip(Igs, sns.color_palette()))

def MurineIgLegend():
    # Make Legend by Ig subclass
    import matplotlib.lines as mlines
    Igs = {'IgG1':'o', 'IgG2a':'d', 'IgG2b':'v', 'IgG3':'s'}
    Igc = {'IgG1':'r', 'IgG2a':'y', 'IgG2b':'g', 'IgG3':'b'}
    patches = list()

    for j in Igs:
        patches.append(mlines.Line2D([], [], color = Igc[j], marker=Igs[j], markersize=7, label=j, linestyle='None'))

    return patches

def ClassAvidityPCA(Mod, ax=None):
    """ Plot the generated binding data for different classes and avidities in PCA space. """
    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()
    
    scores, _ = Mod.PCA()

    for _, row in scores.iterrows():
        colorr = Igidx[row['Ig']]
        ax.errorbar(x=row['PC1'], y=row['PC2'], marker='.', mfc=colorr)

    ax.set_ylabel('PC 2')
    ax.set_xlabel('PC 1')

def InVivoPredictVsActual(Mod, ax=None):
    """ Plot predicted vs actual for regression of conditions in vivo. """

    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()

    _, _, tbN, _, _, _ = Mod.KnockdownLassoCrossVal(printt=True)

    tbN.plot(ax=ax, x='Effectiveness', y='CrossPredict', kind='scatter')

    ax.set_ylim(0, 1.1)
    ax.set_xlim(0, 1.1)
    ax.set_ylabel('Predicted Effect')
    ax.set_xlabel('Actual Effect')

def InVivoPredictComponents(Mod, ax=None):
    """ Plot model components. """

    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()

    _, _, _, components, _, _ = Mod.KnockdownLassoCrossVal()

    sns.barplot(ax=ax, y='Weight', x='Name', data=components)

    ax.set_xticklabels(ax.get_xticklabels(),
                       rotation=40,
                       rotation_mode="anchor",
                       ha="right")

    ax.set_ylabel('Weightings')
    ax.set_xlabel('Components')

def RequiredComponents(ax=None):
    """ Plot model components. """

    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()

    ax.set_ylabel('LOO Perc Explained')
    ax.set_xlabel('Components')

def InVivoPredictVsActualAffinities(Mod, ax=None):
    """ Plot predicted vs actual for regression of conditions in vivo using affinity. """

    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()

    _, _, data = Mod.NimmerjahnPredictByAffinities()

    data.plot(kind='scatter', x='Effectiveness', y='CrossPredict', ax=ax)
    ax.set_ylabel('Predicted Effect')
    ax.set_xlabel('Actual Effect')

def ClassAvidityPredict(Mod, ax=None):
    """ Plot prediction of in vivo model with varying avidity and class. """
    from ..StoneModMouse import MultiAvidityPredict, StoneModelMouse
    from copy import deepcopy

    Mod = deepcopy(Mod)

    # If no axis was provided make our own
    if ax is None:
        ax = plt.gca()

    _, _, _, _, model, normV = Mod.KnockdownLassoCrossVal()

    Mod.v = 30

    table = MultiAvidityPredict(Mod, np.insert(model.coef_, 0, model.intercept_), normV)

    for _, row in table.iterrows():
        colorr = Igidx[row['Ig']]
        ax.errorbar(x=row['Avidity'], y=row['Predict'], marker='.', mfc=colorr)


    ax.set_ylabel('Predicted Effect')


