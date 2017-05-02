import matplotlib
matplotlib.use('AGG')
import seaborn as sns
import pandas as pd
import numpy as np
from ..StoneModMouse import StoneModelMouse

# Predict in vivo response

def makeFigure():
    import string
    import matplotlib.pyplot as plt
    from matplotlib import gridspec
    from .FigureCommon import subplotLabel

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Setup plotting space
    f = plt.figure(figsize=(7, 6))

    # Make grid
    gs1 = gridspec.GridSpec(3, 3)

    # Get list of axis objects
    ax = [ f.add_subplot(gs1[x]) for x in range(9) ]

    # Blank out for the cartoon
    ax[0].axis('off')

    # Plot A/I vs effectiveness.
    AIplot(ax[1])

    # Show performance of affinity prediction
    InVivoPredictVsActualAffinities(ax[2])

    # Make binding data PCA plot
    # ClassAvidityPCA(Mod, ax[3])

    # Show model components
    InVivoPredictComponents(ax[4])

    # Show performance of in vivo regression model
    InVivoPredictVsActual(ax[5])

    # Leave components out plot
    RequiredComponents(ax[6])

    # Predicted contribution plot
    ComponentContrib(ax[7])

    # Predict class/avidity effect
    #ClassAvidityPredict(Mod, model, normV, ax[8])

    for ii, item in enumerate(ax):
        subplotLabel(item, string.ascii_uppercase[ii])

    # Tweak layout
    plt.tight_layout()

    return f

Igs = {'IgG1':'o', 'IgG2a':'d', 'IgG2b':'^', 'IgG3':'s', 'None':'.'}
Ig = {'IgG1', 'IgG2a', 'IgG2b', 'IgG3', 'None'} 
Igidx = dict(zip(Ig, sns.color_palette()))
Knockdown = ['Wild-type', 'FcgRIIB-/-', 'FcgRI-/-', 'FcgRIII-/-', 'FcgRI,IV-/-', 'Fucose-/-']
Knockdownidx = dict(zip(Knockdown, sns.color_palette()))
KnockdownidxL = ['Wild-type', r'Fc$\gamma$RIIB-/-',r'Fc$\gamma$RI-/-',r'Fc$\gamma$RIII-/-',r'Fc$\gamma$RI,IV-/-','Fucose-/-']
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

def PrepforLegend(table):
    knockdowntype = []
    table['Knockdown'] = table.apply(lambda x: x.name.replace(x.name.split('-')[0], ''), axis = 1)
    for i in table['Knockdown']:
        if i == '':
            knockdowntype.append('Wild-type')
        else:
            knockdowntype.append(i[1:])
    table['Knockdown'] = knockdowntype
    return table

def ClassAvidityPCA(Mod, ax):
    """ Plot the generated binding data for different classes and avidities in PCA space. """
    # If no axis was provided make our own
    
    scores, _ = Mod.KnockdownPCA()

    for _, row in scores.iterrows():
        colorr = Knockdownidx[row['Knockdown']]
        fill = {float(1): 'white', float(Mod.v): Knockdownidx[row['Knockdown']]}
        ax.errorbar(x=row['PC1'], y=row['PC2'], marker=Igs[row['Ig']], markeredgewidth = 0.8, mfc=fill[row['Avidity']], mec = colorr, ms=2.5)

    ax.set_ylabel('PC 2')
    ax.set_xlabel('PC 1')
    
    ax.legend(handles=MurineFcIgLegend(Mod), bbox_to_anchor=(3.7, 2.4), loc=2)

def InVivoPredictVsActual(ax):
    """ Plot predicted vs actual for regression of conditions in vivo. """
    from ..StoneModMouseFit import InVivoPredict

    # Run the in vivo regression model
    devar, cevar, tbN = InVivoPredict()

    tbN['Ig'] = tbN.apply(lambda x: x.name.split('-')[0], axis=1)

    for _, row in tbN.iterrows():
        colorr = Igidx[row['Ig']]
        ax.errorbar(x=row['DPredict'], y=row['Effectiveness'], marker='.', mfc=colorr)

    ax.plot([-1, 2], [-1, 2], color='k', linestyle='-', linewidth=1)

    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylabel('Effectiveness')
    ax.set_xlabel('Predicted Effect')


def ComponentContrib(ax):
    """ Plot the predicted contribution of NK cells. """
    from ..StoneModMouseFit import InVivoPredict

    # Run the in vivo regression model
    _, _, tbN = InVivoPredict()

    tbN = tbN.drop('None')

    tbN.index.name = 'condition'
    tbN.reset_index(inplace=True)

    tbN.plot(x='Effectiveness', y="NKfrac", ax=ax, kind='scatter')

    ax.set_xlabel('Effectiveness')
    ax.set_ylabel('Predicted NK Contribution')


def InVivoPredictComponents(ax):
    """ Plot model components. """
    from ..StoneModMouseFit import InVivoPredict

    # Run the in vivo regression model
    _, _, tbN = InVivoPredict()
    tbN = tbN[['NKeff', 'DCeff', '2Beff']]

    tbN.index.name = 'condition'
    tbN.reset_index(inplace=True)

    tbN = pd.melt(tbN, id_vars=['condition'])

    sns.factorplot(x="condition",
                   hue="variable",
                   y="value",
                   data=tbN,
                   ax=ax,
                   kind='bar')

    ax.set_ylabel('Weightings')
    ax.set_xlabel('Components')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, rotation_mode="anchor", ha="right")


def RequiredComponents(ax):
    """ Plot model components. """
    from ..StoneModMouseFit import InVivoPredictMinusComponents

    table = InVivoPredictMinusComponents()

    table.plot(kind='bar', y='CrossVal', ax=ax)

    ax.set_ylabel('LOO Var Explained')
    ax.set_ylim(-1.0, 1.0)


def AIplot(ax):
    """ Plot A/I vs effectiveness. """
    Mod = StoneModelMouse()

    table = Mod.NimmerjahnEffectTableAffinities()
    table = table.loc[table.FcgRIIB > 0, :]
    table['AtoI'] = table.apply(lambda x: max(x.FcgRI, x.FcgRIII, x.FcgRIV)/x.FcgRIIB, axis=1)
    table['Ig'] = table.apply(lambda x: x.name.split('-')[0], axis=1)
    table = PrepforLegend(table)
    for _, row in table.iterrows():
        markerr=Igs[row['Ig']]
        colorr = Knockdownidx[row['Knockdown']]
        ax.errorbar(x=row['AtoI'], y=row['Effectiveness'], marker = markerr, mfc = colorr, ms = 3.5)

    ax.set_ylabel('Effectiveness')
    ax.set_xlabel('A/I Ratio')
    ax.set_xscale('log')


def InVivoPredictVsActualAffinities(ax):
    """ Plot predicted vs actual for regression of conditions in vivo using affinity. """
    from ..StoneModMouseFit import NimmerjahnPredictByAffinities

    dperf, cperf, data = NimmerjahnPredictByAffinities()

    data['Ig'] = data.apply(lambda x: x.name.split('-')[0], axis=1)

    data = PrepforLegend(data)
    for _, row in data.iterrows():
        markerr=Igs[row['Ig']]
        colorr = Knockdownidx[row['Knockdown']]
        ax.errorbar(x=row['DirectPredict'], y=row['Effectiveness'], marker=markerr, mfc=colorr, ms = 3.5)

    ax.plot([-1, 2], [-1, 2], color='k', linestyle='-', linewidth=1)

    ax.set_xlabel('Regressed Effect')
    ax.set_ylabel('Effectiveness')
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)

def ClassAvidityPredict(Mod, model, normV, ax):
    """ Plot prediction of in vivo model with varying avidity and class. """
    from ..StoneModMouse import MultiAvidityPredict
    from copy import deepcopy

    #Mod = deepcopy(Mod)

    #Mod.v = 30

    #table = MultiAvidityPredict(Mod, model, normV)

    #for _, row in table.iterrows():
    #    colorr = Igidx[row['Ig']]
    #    ax.errorbar(x=row['Avidity'], y=row['Predict'], marker='.', mfc=colorr)

    #ax.set_ylabel('Predicted Effect')


