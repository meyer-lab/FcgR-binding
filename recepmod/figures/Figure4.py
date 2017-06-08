import seaborn as sns
import pandas as pd
import numpy as np
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

IgList = ['IgG1', 'IgG2a', 'IgG2b', 'IgG3', 'None']
Igs = {'IgG1':'o', 'IgG2a':'d', 'IgG2b':'^', 'IgG3':'s', 'None':'.'}
Ig = {'IgG1', 'IgG2a', 'IgG2b', 'IgG3', 'None'} 
Igidx = dict(zip(Ig, sns.color_palette()))
Knockdown = ['Wild-type', 'FcgRIIB-/-', 'FcgRI-/-', 'FcgRIII-/-', 'FcgRI,IV-/-', 'Fucose-/-']
Knockdownidx = dict(zip(Knockdown, sns.color_palette()))
KnockdownL = ['Wild-type', r'Fc$\gamma$RIIB-/-',r'Fc$\gamma$RI-/-',r'Fc$\gamma$RIII-/-',r'Fc$\gamma$RI,IV-/-','Fucose-']
KnockdownidxL = dict(zip(KnockdownL, sns.color_palette()))
celltypes = ['NK effect', 'DC effect', '2B-KO effect']
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
    from .FigureCommon import PCApercentVar
    # If no axis was provided make our own
    
    scores, explainedVar = StoneModelMouse().KnockdownPCA()

    commonPlot(ax, scores, 'PC1', 'PC2')
    
    labels = PCApercentVar(explainedVar)
    ax.set_ylabel(labels[1])
    ax.set_xlabel(labels[0])


def InVivoPredictVsActual(ax):
    """ Plot predicted vs actual for regression of conditions in vivo. """
    from ..StoneModMouseFit import InVivoPredict

    # Run the in vivo regression model
    devar, cevar, tbN, _ = InVivoPredict()

    commonPlot(ax, tbN, 'DPredict', 'Effectiveness')

    ax.plot([-1, 2], [-1, 2], color='k', linestyle='-', linewidth=1)

    ax.set_ylabel('Effectiveness')
    ax.set_xlabel('Predicted Effect')
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(-0.05, 1.05)
    devar = r'$\sigma_d$ = '+str(round(devar, 3))
    cevar = r'$\sigma_c$ = '+str(round(cevar, 3))
    ax.text(0.05, 0.9, devar)
    ax.text(0.05, 0.8, cevar)


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

    # Run the in vivo regression model
    _, _, tbN, _ = InVivoPredict()
    tbN = PrepforLegend(tbN)
    fcgrs = tbN['Knockdown']
    tbN = tbN[['NKeff', 'DCeff', '2Beff']]
    
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
    dperf = r'$\sigma_d$ = '+str(round(dperf, 3))
    cperf = r'$\sigma_c$ = '+str(round(cperf, 3))
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
    dperf = r'$\sigma_d$ = '+str(round(dperf, 3))
    cperf = r'$\sigma_c$ = '+str(round(cperf, 3))
    ax.text(0.05, 0.9, dperf)
    ax.text(0.05, 0.8, cperf)

    ax.legend(handles=Legend(KnockdownL, KnockdownidxL, IgList, Igs), bbox_to_anchor=(1, 1), loc=2)


def ClassAvidityPredict(ax):
    """ Plot prediction of in vivo model with varying avidity and class. """
    from ..StoneModMouseFit import InVivoPredict
    from ..StoneHelper import getMedianKx

    L0 = 1.0E-12

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

    data['2B-KO'] = 0


    def NKapply(row):
        from ..StoneModel import StoneMod

        return StoneMod(logR=4.0, Ka=row.FcgRIII, v=row.v, Kx=getMedianKx(), L0=L0, fullOutput = True)[2]

    def CALCapply(row):
        from ..StoneNRecep import StoneN

        return StoneN(logR=[2.0, 3.0, 2.0, 2.0],
                      Ka=[row.FcgRI+0.00001, row.FcgRIIB, row.FcgRIII, row.FcgRIV],
                      Kx=getMedianKx(),
                      gnu=row.v,
                      L0=L0).getActivity([1, -1, 1, 1])

    data['NK'] = data.apply(NKapply, axis=1)
    data['DC'] = data.apply(CALCapply, axis=1)

    data['predict'] = model.predict(data[['NK', 'DC', '2B-KO']].as_matrix())
    data.reset_index(level=0, inplace=True)

    # Plot the calculated crossvalidation performance
    sns.FacetGrid(data, hue='index').map(ax.plot, 'v', 'predict')

    ax.vlines(5.0, 0, 1)

    ax.set_ylabel('Predicted Effectiveness')
    ax.set_xlabel('Avidity')
