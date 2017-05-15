import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ..StoneModMouse import StoneModelMouse

# Predict in vivo response

def makeFigure():
    import string
    from .FigureCommon import subplotLabel, getSetup

    # Get list of axis objects
    ax, f = getSetup((7, 6), (3, 3))

    # Blank out for the cartoon
    ax[0].axis('off')

    # Plot A/I vs effectiveness.
    AIplot(ax[1])

    # Show performance of affinity prediction
    InVivoPredictVsActualAffinities(ax[2])

    # Make binding data PCA plot
    ClassAvidityPCA(ax[3])

    # Show model components
    InVivoPredictComponents(ax[4])

    # Show performance of in vivo regression model
    InVivoPredictVsActual(ax[5])

    # Leave components out plot
    RequiredComponents(ax[6])

    # Predicted contribution plot
    ComponentContrib(ax[7])

    # Predict class/avidity effect
    ClassAvidityPredict(ax[8])

    for ii, item in enumerate(ax):
        subplotLabel(item, string.ascii_uppercase[ii])

    # Tweak layout
    f.tight_layout()

    return f

Igs = {'IgG1':'o', 'IgG2a':'d', 'IgG2b':'^', 'IgG3':'s', 'None':'.'}
Ig = {'IgG1', 'IgG2a', 'IgG2b', 'IgG3', 'None'} 
Igidx = dict(zip(Ig, sns.color_palette()))
Knockdown = ['Wild-type', 'FcgRIIB-/-', 'FcgRI-/-', 'FcgRIII-/-', 'FcgRI,IV-/-', 'Fucose-/-']
Knockdownidx = dict(zip(Knockdown, sns.color_palette()))
KnockdownL = ['Wild-type', r'Fc$\gamma$RIIB-/-',r'Fc$\gamma$RI-/-',r'Fc$\gamma$RIII-/-',r'Fc$\gamma$RI,IV-/-','Fucose-']
KnockdownidxL = dict(zip(KnockdownL, sns.color_palette()))
celltypes = ['NK effect', 'DC effect', '2B effect']
celltypeidx = dict(zip(celltypes, sns.color_palette()))

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

def ClassAvidityPCA(ax):
    """ Plot the generated binding data for different classes and avidities in PCA space. """
    # If no axis was provided make our own
    
    scores, expvar = StoneModelMouse().KnockdownPCA()

    commonPlot(ax, scores, 'PC1', 'PC2')

    ax.set_ylabel('PC 2')
    ax.set_xlabel('PC 1')


def InVivoPredictVsActual(ax):
    """ Plot predicted vs actual for regression of conditions in vivo. """
    from ..StoneModMouseFit import InVivoPredict

    # Run the in vivo regression model
    devar, cevar, tbN = InVivoPredict()

    commonPlot(ax, tbN, 'DPredict', 'Effectiveness')

    ax.plot([-1, 2], [-1, 2], color='k', linestyle='-', linewidth=1)

    ax.set_ylabel('Effectiveness')
    ax.set_xlabel('Predicted Effect')
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(-0.05, 1.05)
    devar = r'$\sigma$d = '+str(round(devar, 3))
    cevar = r'$\sigma$c = '+str(round(cevar, 3))
    ax.text(0.05, 0.9, devar)
    ax.text(0.05, 0.8, cevar)


def ComponentContrib(ax):
    """ Plot the predicted contribution of NK cells. """
    from ..StoneModMouseFit import InVivoPredict

    # Run the in vivo regression model
    _, _, tbN = InVivoPredict()

    tbN = tbN.drop('None')

    commonPlot(ax, tbN, 'NKfrac', 'Effectiveness')

    ax.set_ylabel('Effectiveness')
    ax.set_xlabel('Predicted NK Contribution')


def InVivoPredictComponents(ax):
    """ Plot model components. """
    from ..StoneModMouseFit import InVivoPredict
    import matplotlib

    # Run the in vivo regression model
    _, _, tbN = InVivoPredict()
    tbN = PrepforLegend(tbN)
    fcgrs = tbN['Knockdown']
    tbN = tbN[['NKeff', 'DCeff', '2Beff']]
    
    # Set up x axis labels 
    for i in range(len(fcgrs)):
        for j in range(len(Knockdown)):
            if fcgrs[i] == Knockdown[j]:
                fcgrs[i] = KnockdownL[j]
    idx = list(tbN.index.copy())
    for k in range(len(idx)):
        if fcgrs[k] != 'Wild-type':
            fc = idx[k].replace(idx[k].split('-')[0], '')
            idx[k] = idx[k].replace(fc, str('-'+fcgrs[k]))
    tbN.index = idx
    
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
    # Make legend
    patches = list()
    for key, val in celltypeidx.items():
        patches.append(matplotlib.patches.Patch(color=val, label=key))
    ax.legend(handles=patches, bbox_to_anchor=(0, 1), loc=2)

def RequiredComponents(ax):
    """ Plot model components. """
    from ..StoneModMouseFit import InVivoPredictMinusComponents

    table = InVivoPredictMinusComponents()

    table.plot(kind='bar', y='CrossVal', ax=ax, legend=False)

    ax.set_ylabel('LOO Var Explained')
    ax.set_ylim(-1.0, 1.0)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, rotation_mode="anchor", ha="right")


def commonPlot(ax, table, xcol, ycol):
    table['Ig'] = table.apply(lambda x: x.name.split('-')[0], axis=1)
    table = PrepforLegend(table)

    for _, row in table.iterrows():
        markerr=Igs[row['Ig']]
        colorr = Knockdownidx[row['Knockdown']]
        ax.errorbar(x=row[xcol], y=row[ycol], marker=markerr, mfc = colorr, ms=3.5)


def AIplot(ax):
    """ Plot A/I vs effectiveness. """
    from ..StoneModMouseFit import NimmerjahnPredictByAIratio
    
    dperf, cperf, table, coe, inter = NimmerjahnPredictByAIratio()
    
    commonPlot(ax, table, 'AtoI', 'Effectiveness')
    x = [10**(-2), 10**3]
    ax.plot(x, coe * np.log10(x) + inter, color='k', linestyle='-', linewidth=1)
    ax.set_ylabel('Effectiveness')
    ax.set_xlabel('A/I Ratio')
    ax.set_xscale('log')
    ax.set_xlim(10**(-1.2), 10**(2.6))
    ax.set_ylim(-0.05, 1.05)
    dperf = r'$\sigma$d = '+str(round(dperf, 3))
    cperf = r'$\sigma$c = '+str(round(cperf, 3))
    ax.text(0.1, 0.9, dperf)
    ax.text(0.1, 0.8, cperf)

def InVivoPredictVsActualAffinities(ax):
    """ Plot predicted vs actual for regression of conditions in vivo using affinity. """
    from ..StoneModMouseFit import NimmerjahnPredictByAffinities
    from .FigureCommon import Legend

    dperf, cperf, data = NimmerjahnPredictByAffinities()

    commonPlot(ax, data, 'DirectPredict', 'Effectiveness')

    ax.plot([-1, 2], [-1, 2], color='k', linestyle='-', linewidth=1)

    ax.set_xlabel('Regressed Effect')
    ax.set_ylabel('Effectiveness')
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    dperf = r'$\sigma$d = '+str(round(dperf, 3))
    cperf = r'$\sigma$c = '+str(round(cperf, 3))
    ax.text(0.05, 0.9, dperf)
    ax.text(0.05, 0.8, cperf)
    
    ax.legend(handles=Legend(KnockdownidxL, Igs), bbox_to_anchor=(1, 1), loc=2)


def ClassAvidityPredict(ax):
    """ Plot prediction of in vivo model with varying avidity and class. """
    

    ax.set_ylabel('Predicted Effect')