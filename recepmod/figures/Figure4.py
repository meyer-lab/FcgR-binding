import seaborn as sns
import pandas as pd
import numpy as np
from ..StoneModMouse import StoneModelMouse

# Predict in vivo response


def makeFigure():
    import string
    from .FigureCommon import subplotLabel, getSetup
    import matplotlib.gridspec as gridspec
    from matplotlib.pyplot import subplot

    # Get list of axis objects; by 0-index, 3 and 11 empty, 4 double
    ax, f = getSetup((9, 6), (3, 4), mults=[5], multz={5:2}, empts=[3,11])

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
        if ii != 4:
            subplotLabel(item, string.ascii_uppercase[ii])
        else:
            subplotLabel(item, string.ascii_uppercase[ii], hstretch=2.5)

    # Tweak layout
    f.tight_layout()

    return f

IgList = ['IgG1', 'IgG2a', 'IgG2b', 'IgG3', 'None']
iggRename = lambda name: 'm'+name if name[0]=='I' else name
Igs = {'IgG1': 'o', 'IgG2a': 'd', 'IgG2b': '^', 'IgG3': 's', 'None': '.'}
keys = [key for key in Igs.keys()]
for key in keys:
    Igs[iggRename(key)] = Igs[key]

Ig = {'IgG1', 'IgG2a', 'IgG2b', 'IgG3', 'None'}
Igidx = dict(zip(Ig, sns.color_palette()))
Knockdown = ['Wild-type', 'FcgRIIB-/-', 'FcgRI-/-', 'FcgRIII-/-', 'FcgRI,IV-/-', 'Fucose-/-']
Knockdownidx = dict(zip(Knockdown, sns.color_palette()))
KnockdownL = ['Wild-type', r'mFc$\gamma$RIIB-/-',r'mFc$\gamma$RI-/-',r'mFc$\gamma$RIII-/-',r'mFc$\gamma$RI,IV-/-','Fucose-']
KnockdownidxL = dict(zip(KnockdownL, sns.color_palette()))
celltypes = ['NK effect', 'DC-like effect']
celltypes2 = ['NKeff','DCeff']
cellColors = sns.crayon_palette(['Royal Purple','Brown','Asparagus'])
celltypeidx = dict(zip(celltypes, cellColors))
for cell, cell2 in zip(celltypes,celltypes2):
    celltypeidx[cell2] = celltypeidx[cell]


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
    from .FigureCommon import PCApercentVar
    # If no axis was provided make our own

    scores, explainedVar = StoneModelMouse().KnockdownPCA()

    commonPlot(ax, scores, 'PC1', 'PC2')

    labels = PCApercentVar(explainedVar)
    ax.set_ylabel(labels[1])
    ax.set_xlabel(labels[0])
    ax.set_xticklabels([str(tick/1e8)[0:(4 if tick<0 else 3)] for tick in ax.get_xticks()])
    ax.set_yticklabels([str(tick/1e8)[0:(4 if tick<0 else 3)] for tick in ax.get_yticks()])


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
    devar = r'$R^2_d$ = '+str(round(devar, 3))
    cevar = r'$R^2_c$ = '+str(round(cevar, 3))
    ax.text(0.05, 0.9, devar)
    ax.text(0.05, 0.75, cevar)


def ComponentContrib(ax):
    """ Plot the predicted contribution of NK cells. """
    from ..StoneModMouseFit import InVivoPredict

    # Run the in vivo regression model
    _, _, tbN, _ = InVivoPredict()

    tbN = tbN.drop('None')

    commonPlot(ax, tbN, 'NKfrac', 'Effectiveness')

    ax.set_ylabel('Effectiveness')
    ax.set_xlabel('Predicted NK Contribution')


def InVivoPredictComponents(ax):
    """ Plot model components. """
    from ..StoneModMouseFit import InVivoPredict
    import matplotlib
    from .FigureCommon import alternatingRects

    # Run the in vivo regression model
    _, _, tbN, _ = InVivoPredict()
    # Remove the "None' condition
    tbN = tbN[tbN.index != 'None']
    tbN = PrepforLegend(tbN)
    fcgrs = tbN['Knockdown'].tolist()
    tbN = tbN[['NKeff', 'DCeff']]

    # Set up x axis labels 
    for i in range(len(fcgrs)):
        for j in range(len(Knockdown)):
            if fcgrs[i] == Knockdown[j]:
                fcgrs[i] = KnockdownL[j]
    idx = list(tbN.index.copy())

    for k, item in enumerate(idx):
        if fcgrs[k] != 'Wild-type':
            fc = item.replace(item.split('-')[0], '')
            idx[k] = item.replace(fc, str('-'+fcgrs[k]))

    tbN.index = idx

    tbN.index.name = 'condition'
    tbN.reset_index(inplace=True)

    tbN = pd.melt(tbN, id_vars=['condition'])

    sns.factorplot(x="condition",
                   hue="variable",
                   y="value",
                   data=tbN,
                   ax=ax,
                   kind='bar',
                   palette=celltypeidx)

    ax.set_ylabel('Weightings')
    ax.set_xlabel('')

    for lab in ax.get_xticklabels():
        lab.set_text('m' + lab.get_text() if lab.get_text()[0]=='I' else lab.get_text())

    # Make legend
    patches = list()
    for key, val in zip(celltypes, [celltypeidx[typ] for typ in celltypes]):
        patches.append(matplotlib.patches.Patch(color=val, label=key))
    ax.legend(handles=patches, bbox_to_anchor=(0, 1), loc=2)

    # Set alternating grey rectangles in the background to allow for better
    # readability of the bar graph
    from itertools import chain
    ax.set_xticks(list(chain.from_iterable((num, num+0.5) for num in ax.get_xticks())))
    ax.set_xticklabels(list(chain.from_iterable((name, '') for name in ax.get_xticklabels())))
    ax.set_xticklabels(ax.get_xticklabels(),
                       rotation=40, rotation_mode="anchor", ha="right",
                       position=(0, 0.05), fontsize=6.5)

    ax.set_xlim(ax.get_xlim())
    ax.set_ylim(ax.get_ylim())
    alternatingRects([ax.get_xlim()[0]]+[x for x in ax.get_xticks() if x%1!=0]+[ax.get_xlim()[-1]],
                     ylims=ax.get_ylim(),ax=ax)
    for rect in ax.get_children()[0:24]:
        ax.add_patch(rect)


def RequiredComponents(ax):
    """ Plot model components. """
    from ..StoneModMouseFit import InVivoPredictMinusComponents

    table = InVivoPredictMinusComponents()

    table.plot(kind='bar', y='CrossVal', ax=ax, legend=False)

    ax.set_ylabel('LOO $R^2$ Explained')
    ax.set_ylim(0.0, 1.0)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, rotation_mode="anchor", ha="right")


def commonPlot(ax, table, xcol, ycol):
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
    dperf = r'$R^2_d$ = '+str(round(dperf, 3))
    cperf = r'$R^2_c$ = '+str(round(cperf, 3))
    ax.text(0.1, 0.9, dperf)
    ax.text(0.1, 0.75, cperf)

def InVivoPredictVsActualAffinities(ax):
    """ Plot predicted vs actual for regression of conditions in vivo using affinity. """
    from ..StoneModMouseFit import NimmerjahnPredictByAffinities
    from .FigureCommon import Legend

    dperf, cperf, data = NimmerjahnPredictByAffinities()

    commonPlot(ax, data, 'DirectPredict', 'Effectiveness')

    ax.plot([-1, 2], [-1, 2], color='k', linestyle='-', linewidth=1)

    ax.set_xlabel('Regressed Effectiveness')
    ax.set_ylabel('Effectiveness')
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    dperf = r'$R^2_d$ = '+str(round(dperf, 3))
    cperf = r'$R^2_c$ = '+str(round(cperf, 3))
    ax.text(0.05, 0.9, dperf)
    ax.text(0.05, 0.75, cperf)

    ax.legend(handles=Legend(KnockdownL, KnockdownidxL,
                             [iggRename(igg) for igg in IgList], Igs),
              bbox_to_anchor=(1.5, 1), loc=2)


def ClassAvidityPredict(ax):
    """ Plot prediction of in vivo model with varying avidity and class. """
    from ..StoneModMouseFit import InVivoPredict
    from ..StoneModMouseFit import CALCapply
    from .FigureCommon import Legend

    # Run the in vivo regression model
    _, _, _, model = InVivoPredict()
    data = StoneModelMouse().NimmerjahnEffectTableAffinities()
    data = data[data.index.str.contains("FcgR") == False]
    data.drop('Effectiveness', axis=1, inplace=True)

    data['v'] = 1
    dataOne = data.copy()

    for vv in range(2, 11):
        dataNew = dataOne.copy()

        dataNew['v'] = vv

        data = data.append(dataNew)

    data['L0'] = 1.0E-12

    data = data.apply(CALCapply, axis=1)

    data['predict'] = model.predict(data[['NK', 'DC']].as_matrix())
    data.reset_index(level=0, inplace=True)

    # Plot the calculated crossvalidation performance
    col = sns.crayon_palette(['Pine Green','Goldenrod','Wild Strawberry',
                                 'Brown', 'Navy Blue'])
    newIgList = IgList[0:-1]+['IgG2b-Fucose-/-']
    colors = dict(zip([iggRename(ig) for ig in newIgList],col))
    
    sns.FacetGrid(data, hue='index', palette=col).map(ax.plot, 'v', 'predict',
                                                      marker='.',
                                                      linestyle='None')

    ax.vlines(5.0, 0, 1)

    ax.set_ylabel('Predicted Effectiveness')
    ax.set_xlabel('Avidity')
    ax.legend(handles=Legend([iggRename(ig) for ig in newIgList],colors,[],[]),
              loc=2, bbox_to_anchor=(1,1))
