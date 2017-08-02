import logging
import seaborn as sns
import pandas as pd
import numpy as np
from itertools import product
from .FigureCommon import Legend
from ..StoneModMouse import StoneModelMouse
from ..StoneModMouseFit import InVivoPredict, cellpops, CALCapply
from matplotlib.patches import Patch

# Predict in vivo response


def makeFigure():
    import string
    from .FigureCommon import subplotLabel, getSetup

    # Get list of axis objects; by 0-index, 3 and 11 empty, 4 double
    ax, f = getSetup((9, 6), (3, 4), mults=[5], multz={5: 2}, empts=[3, 11])

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
    AffinityPredict(ax[8])

    for ii, item in enumerate(ax):
        if ii != 4:
            subplotLabel(item, string.ascii_uppercase[ii])
        else:
            subplotLabel(item, string.ascii_uppercase[ii], hstretch=2.5)

    # Tweak layout
    f.tight_layout()

    return f


def iggRename(x):
    """ Make names refer to murine form. """
    return x.replace('IgG', 'mIgG')


IgList = ['IgG1', 'IgG2a', 'IgG2b', 'IgG3', 'None']
Igs = {'IgG1': 'o', 'IgG2a': 'd', 'IgG2b': '^', 'IgG3': 's', 'None': '.'}
keys = [key for key in Igs.keys()]
for key in keys:
    Igs[iggRename(key)] = Igs[key]

Knockdown = ['Wild-type', 'FcgRIIB-/-', 'FcgRI-/-', 'FcgRIII-/-', 'FcgRI,IV-/-', 'Fucose-/-']


def PrepforLegend(table):
    knockdowntype = []
    table['Knockdown'] = table.apply(lambda x: x.name.replace(x.name.split('-')[0], ''), axis=1)
    for i in table['Knockdown']:
        if i == '':
            knockdowntype.append('Wild-type')
        else:
            knockdowntype.append(i[1:])
    table['Knockdown'] = knockdowntype
    return table


def ClassAvidityPCA(ax):
    """ Plot the generated binding data for different classes and avidities in PCA space. """
    from .FigureCommon import PCApercentVar
    # If no axis was provided make our own

    scores, explainedVar = StoneModelMouse().KnockdownPCA()

    commonPlot(ax, scores, 'PC1', 'PC2')

    labels = PCApercentVar(explainedVar)
    ax.set_ylabel(labels[1])
    ax.set_xlabel(labels[0])
    ax.set_xticklabels([str(tick / 1e8)[0:(4 if tick < 0 else 3)] for tick in ax.get_xticks()])
    ax.set_yticklabels([str(tick / 1e8)[0:(4 if tick < 0 else 3)] for tick in ax.get_yticks()])


def InVivoPredictVsActual(ax):
    """ Plot predicted vs actual for regression of conditions in vivo. """
    from ..StoneModMouseFit import InVivoPredict

    # Run the in vivo regression model
    devar, cevar, tbN, _ = InVivoPredict()

    commonPlot(ax, tbN, 'DPredict', 'Effectiveness')

    ax.plot([-1, 2], [-1, 2], color='k', linestyle='-', linewidth=1)

    ax.set_ylabel('Effectiveness')
    ax.set_xlabel('Predicted Effectiveness')
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(-0.05, 1.05)
    devar = r'$R^2_d$ = ' + str(round(devar, 3))
    cevar = r'$R^2_c$ = ' + str(round(cevar, 3))
    ax.text(0.05, 0.9, devar)
    ax.text(0.05, 0.75, cevar)


def ComponentContrib(ax):
    """ Plot the predicted contribution of NK cells. """
    from ..StoneModMouseFit import InVivoPredict, cellpops

    # Run the in vivo regression model
    _, _, tbN, _ = InVivoPredict()

    tbN = tbN.drop('None')

    tbN['frac'] = tbN['EOeff'] / tbN[[s + 'eff' for s in cellpops]].sum(axis=1)

    commonPlot(ax, tbN, 'frac', 'Effectiveness')

    ax.set_ylabel('Effectiveness')
    ax.set_xlabel('Predicted EO Contribution')


def InVivoPredictComponents(ax):
    """ Plot model components. """
    from ..StoneModMouseFit import InVivoPredict
    import re
    from .FigureCommon import alternatingRects

    # Run the in vivo regression model
    tbN = InVivoPredict()[2]

    # Only keep the effect columns
    tbN = tbN.select(lambda x: re.search('eff', x), axis=1)

    tbN.index = map(lambda x: x.replace('Fcg', r'mFc$\gamma$'), tbN.index)
    tbN.index = map(lambda x: x.replace('ose-/-', 'ose-'), tbN.index)
    tbN.index = map(lambda x: x.replace('IgG', 'mIgG'), tbN.index)

    tbN.index.name = 'condition'
    tbN.reset_index(inplace=True)

    tbN = pd.melt(tbN, id_vars=['condition'])

    # Remove eff from cell line labels
    tbN['variable'] = list(map(lambda x: x.replace('eff', ''), tbN.variable))

    with sns.color_palette("Paired"):
        sns.factorplot(x="condition", hue="variable", y="value", data=tbN,
                       ax=ax, kind='bar', legend=False)

    ax.set_ylabel('Weightings')
    ax.set_xlabel('')
    ax.legend(loc='best')

    # Set alternating grey rectangles in the background to allow for better
    # readability of the bar graph
    ax.set_xticklabels(ax.get_xticklabels(),
                       rotation=40, rotation_mode="anchor", ha="right",
                       position=(0, 0.05), fontsize=6.5)

    numRects = len(tbN['condition'].unique())

    alternatingRects(xlims=ax.get_xlim(), ylims=ax.get_ylim(),
                     numRects=numRects, ax=ax)


def RequiredComponents(ax):
    """ Plot model components. """
    from ..StoneModMouseFit import InVivoPredictMinusComponents

    table = InVivoPredictMinusComponents()

    table.plot(kind='bar', y='CrossVal', ax=ax, legend=False)

    ax.set_ylabel('LOO $R^2$ Explained')
    ax.set_ylim(0.0, 1.0)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, rotation_mode="anchor", ha="right")


def commonPlot(ax, table, xcol, ycol):
    Knockdownidx = dict(zip(Knockdown, sns.color_palette()))

    table['Ig'] = table.apply(lambda x: x.name.split('-')[0], axis=1)
    table = PrepforLegend(table)

    for _, row in table.iterrows():
        markerr = Igs[row['Ig']]
        colorr = Knockdownidx[row['Knockdown']]
        ax.errorbar(x=row[xcol], y=row[ycol], marker=markerr, mfc=colorr,
                    ms=3.5)


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
    dperf = r'$R^2_d$ = ' + str(round(dperf, 3))
    cperf = r'$R^2_c$ = ' + str(round(cperf, 3))

    logging.info('AI crossval: ' + cperf)

    ax.text(0.1, 0.9, dperf)
    ax.text(0.1, 0.75, cperf)


def InVivoPredictVsActualAffinities(ax):
    """ Plot predicted vs actual for regression of conditions in vivo using affinity. """
    from ..StoneModMouseFit import NimmerjahnPredictByAffinities

    dperf, cperf, data = NimmerjahnPredictByAffinities()

    commonPlot(ax, data, 'DirectPredict', 'Effectiveness')

    ax.plot([-1, 2], [-1, 2], color='k', linestyle='-', linewidth=1)

    ax.set_xlabel('Regressed Effectiveness')
    ax.set_ylabel('Effectiveness')
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    dperf = r'$R^2_d$ = ' + str(round(dperf, 3))
    cperf = r'$R^2_c$ = ' + str(round(cperf, 3))

    logging.info('AI with KO crossval: ' + cperf)

    ax.text(0.05, 0.9, dperf)
    ax.text(0.05, 0.75, cperf)

    KnockdownL = ['Wild-type', r'mFc$\gamma$RIIB-/-',
                  r'mFc$\gamma$RI-/-', r'mFc$\gamma$RIII-/-',
                  r'mFc$\gamma$RI,IV-/-', 'Fucose-']

    ax.legend(handles=Legend(KnockdownL, dict(zip(KnockdownL, sns.color_palette())),
                             [iggRename(igg) for igg in IgList], Igs),
              bbox_to_anchor=(1.5, 1), loc=2)


def AffinityPredict(ax):
    """ Make a prediction for varying affinity. """
    # Run the in vivo regression model
    _, _, tblOne, model = InVivoPredict()
    data = StoneModelMouse().NimmerjahnEffectTableAffinities().loc['IgG2b', ]

    edits = pd.DataFrame(list(product(range(4), np.logspace(-1, 1, num=20))),
                         columns=['recep', 'edit'])

    edits['FcgRI'] = data.FcgRI
    edits['FcgRIIB'] = data.FcgRIIB
    edits['FcgRIII'] = data.FcgRIII
    edits['FcgRIV'] = data.FcgRIV

    for ii in range(edits.shape[0]):
        edits.iloc[ii, 2 + edits.recep[ii]] *= edits.edit[ii]

    edits['L0'] = tblOne['L0'][0]
    edits['v'] = tblOne['v'][0]

    # Calculate activity for each cell population
    edits = edits.apply(CALCapply, axis=1)

    # Run through regression model to get predictions
    edits['predict'] = model.predict(edits[cellpops].as_matrix())

    colors = sns.color_palette("Paired")
    with colors:
        # Plot each line
        sns.FacetGrid(edits, hue='recep').map(ax.plot, 'edit', 'predict')

    # TODO: Change the figure caption

    ax.set_ylabel('Predicted Effectiveness')
    ax.set_xlabel('Fold Change in Affinity')
    ax.set_xscale('log')
    patches = [Patch(color=colors[j], label=r'$f='+str(j)+'$') for j in range(1,4)]
    ax.legend(handles=patches)
