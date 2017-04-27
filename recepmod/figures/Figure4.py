import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from ..StoneModMouse import StoneModelMouse

# Predict in vivo response

def makeFigure():
    import string
    from matplotlib import gridspec
    from ..StoneHelper import getMedianKx
    from .FigureCommon import subplotLabel

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Load murine class
    Mod = StoneModelMouse()

    # Setup plotting space
    f = plt.figure(figsize=(7, 6))

    # Make grid
    gs1 = gridspec.GridSpec(3, 3)

    # Get list of axis objects
    ax = [ f.add_subplot(gs1[x]) for x in range(9) ]

    # Blank out for the cartoon
    ax[0].axis('off')

    # Plot A/I vs effectiveness.
    AIplot(Mod, ax[1])

    # Show performance of affinity prediction
    InVivoPredictVsActualAffinities(Mod, ax[2])

    # Make binding data PCA plot
    ClassAvidityPCA(Mod, ax[3])

    # Show performance of in vivo regression model
    InVivoPredictVsActual(Mod, ax[4])

    # Show model components
    InVivoPredictComponents(Mod, ax[5])

    # Leave components out plot
    RequiredComponents(ax[6])

    # Predict class/avidity effect
    ClassAvidityPredict(Mod, ax[7])

    # Blank out for the cartoon
    ax[8].axis('off')

    for ii, item in enumerate(ax):
        subplotLabel(item, string.ascii_uppercase[ii])

    # Tweak layout
    plt.tight_layout()

    return f

Igs = {'IgG1':'o', 'IgG2a':'d', 'IgG2b':'^', 'IgG3':'s'}
Ig = {'IgG1', 'IgG2a', 'IgG2b', 'IgG3'} 
Igidx = dict(zip(Ig, sns.color_palette()))
Knockdown = {'None', 'FcgRIIB-/-', 'FcgRI-/-', 'FcgRIII-/-', 'FcgRI,IV-/-', 'Fucose-/-'}
Knockdownidx = dict(zip(Knockdown, sns.color_palette()))
KnockdownidxL = ['None', r'Fc$\gamma$RIIB-/-',r'Fc$\gamma$RI-/-',r'Fc$\gamma$RIII-/-',r'Fc$\gamma$RI,IV-/-','Fucose-/-']
KnockdownidxL = dict(zip(KnockdownidxL, sns.color_palette()))

def MurineFcIgLegend(Mod):
    # Make Legend by Ig subclass
    import matplotlib.lines as mlines
    import matplotlib.patches as mpatches

    patches = list()

    for f in KnockdownidxL:
        patches.append(mpatches.Patch(color=KnockdownidxL[f], label=f))

    for j in Igs:
        patches.append(mlines.Line2D([], [], color='black', marker=Igs[j], markersize=7, label=j, linestyle='None'))
    patches.append(mpatches.Patch(color='black', label='Avidity 1', fill = False, lw = 1))
    patches.append(mpatches.Patch(color = 'black', label='Avidity '+str(Mod.v)))
    
    return patches

def ClassAvidityPCA(Mod, ax):
    """ Plot the generated binding data for different classes and avidities in PCA space. """
    # If no axis was provided make our own
    
    scores, _ = Mod.KnockdownPCA()

    for _, row in scores.iterrows():
        colorr = Knockdownidx[row['Knockdown']]
        fill = {float(1): 'white', float(Mod.v): Knockdownidx[row['Knockdown']]}
        ax.errorbar(x=row['PC1'], y=row['PC2'], marker=Igs[row['Ig']], markeredgewidth = 1, mfc=fill[row['Avidity']], mec = colorr, ms=3)

    ax.set_ylabel('PC 2')
    ax.set_xlabel('PC 1')
    
    ax.legend(handles=MurineFcIgLegend(Mod), bbox_to_anchor=(3.5, 2.3), loc=2)

def InVivoPredictVsActual(Mod, ax):
    """ Plot predicted vs actual for regression of conditions in vivo. """

    _, _, tbN, _, _, _ = Mod.KnockdownLassoCrossVal(addavidity1=True)
    tbN['Ig'] = tbN.apply(lambda x: x.name.split('-')[0], axis=1)

    for _, row in tbN.iterrows():
        colorr = Igidx[row['Ig']]
        ax.errorbar(x=row['CrossPredict'], y=row['Effectiveness'], marker='.', mfc=colorr)

    ax.plot([-1, 2], [-1, 2], color='k', linestyle='-', linewidth=1)

    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylabel('Effectiveness')
    ax.set_xlabel('Predicted Effect')

def InVivoPredictComponents(Mod, ax):
    """ Plot model components. """

    _, _, _, components, _, _ = Mod.KnockdownLassoCrossVal(addavidity1=True)

    sns.barplot(ax=ax, y='Weight', x='Name', data=components)

    ax.set_xticklabels(ax.get_xticklabels(),
                       rotation=40,
                       rotation_mode="anchor",
                       ha="right")

    ax.set_ylabel('Weightings')
    ax.set_xlabel('Components')


def AIplot(Mod, ax):
    """ Plot A/I vs effectiveness. """

    table = Mod.NimmerjahnEffectTableAffinities()
    table = table.loc[table.FcgRIIB > 0, :]
    table['AtoI'] = table.apply(lambda x: max(x.FcgRI, x.FcgRIII, x.FcgRIV)/x.FcgRIIB, axis=1)
    table['Ig'] = table.apply(lambda x: x.name.split('-')[0], axis=1)

    for _, row in table.iterrows():
        colorr = Igidx[row['Ig']]
        ax.errorbar(x=row['AtoI'], y=row['Effectiveness'], marker='.', mfc=colorr)

    ax.set_ylabel('Effectiveness')
    ax.set_xlabel('A/I Ratio')
    ax.set_xscale('log')

def RequiredComponents(ax):
    """ Plot model components. """

    ax.set_ylabel('LOO Perc Explained')
    ax.set_xlabel('Components')

def InVivoPredictVsActualAffinities(Mod, ax):
    """ Plot predicted vs actual for regression of conditions in vivo using affinity. """

    _, _, data = Mod.NimmerjahnPredictByAffinities()
    data['Ig'] = data.apply(lambda x: x.name.split('-')[0], axis=1)

    for _, row in data.iterrows():
        colorr = Igidx[row['Ig']]
        ax.errorbar(x=row['DirectPredict'], y=row['Effectiveness'], marker='.', mfc=colorr)

    ax.plot([-1, 2], [-1, 2], color='k', linestyle='-', linewidth=1)

    ax.set_xlabel('Regressed Effect')
    ax.set_ylabel('Effectiveness')
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)

def ClassAvidityPredict(Mod, ax):
    """ Plot prediction of in vivo model with varying avidity and class. """
    from ..StoneModMouse import MultiAvidityPredict, StoneModelMouse
    from copy import deepcopy

    Mod = deepcopy(Mod)

    _, _, _, _, model, normV = Mod.KnockdownLassoCrossVal(addavidity1=True)

    Mod.v = 30

    table = MultiAvidityPredict(Mod, np.insert(model.coef_, 0, model.intercept_), normV)

    for _, row in table.iterrows():
        colorr = Igidx[row['Ig']]
        ax.errorbar(x=row['Avidity'], y=row['Predict'], marker='.', mfc=colorr)


    ax.set_ylabel('Predicted Effect')