import matplotlib
matplotlib.use('AGG')
import numpy as np
import pandas as pd
import seaborn as sns

# Compare across species

def makeFigure():
    import string
    from itertools import product
    from matplotlib import gridspec
    import matplotlib.pyplot as plt
    from .FigureCommon import subplotLabel, makeFcIgLegend

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")
    pd.set_option('expand_frame_repr', False)

    # Setup the table of conditions we'll use.
    avidity = np.logspace(0, 3, 4, base=2, dtype=np.int)
    ligand = np.logspace(start=-12, stop=-5, num=3)
    IgID = np.arange(0, 4, dtype=np.int)
    conditions = pd.DataFrame(list(product(avidity, ligand, IgID)), columns=['avidity', 'ligand', 'IgID'])

    # Setup plotting space
    f = plt.figure(figsize=(7, 5))

    # Make grid
    gs1 = gridspec.GridSpec(2, 4, width_ratios=[32, 11, 32, 11])

    # Get list of axis objects
    ax = [f.add_subplot(gs1[2*x]) for x in range(4)]

    PCAmurine(ax[0:2], conditions)

    PCAhuman(ax[2:4], conditions)

    subplotLabel(ax[0], 'A')
    subplotLabel(ax[2], 'B')

    for ii, item in enumerate(ax):
        ax[ii].set_ylabel('PC 2')
        ax[ii].set_xlabel('PC 1')

    # Tweak layout
    f.tight_layout()

    return f

def calcActivity(affinities, expressions, conditions, activities):
    """ Calculate the ligand bound and activity response for different cell populations. """
    from ..StoneHelper import getMedianKx
    from ..StoneNRecep import StoneN
    from ..StoneModel import StoneMod

    def applyF(condR):
        for exprN, expr in expressions.items():
            # Isolate receptors expressed, and keep the index of those
            exprV = np.array(expr, dtype=np.float)
            exprIDX = np.logical_not(np.isnan(exprV))
            exprV = exprV[exprIDX]

            # Pull out the relevant affinities from the table
            affyH = affinities[exprIDX, int(condR.IgID)] + 0.1

            try:
                if exprV.size > 1:
                    # Setup the StoneN model
                    M = StoneN(logR=exprV, Ka=affyH, Kx=getMedianKx(), gnu=condR.avidity, L0=condR.ligand)

                    condR[exprN + '_activity'] = M.getActivity(activities[exprN])
                    condR[exprN + '_Lbnd'] = M.getLbnd()
                else:
                    output = StoneMod(exprV, affyH, condR.avidity, getMedianKx(), condR.ligand, fullOutput=True)

                    condR[exprN + '_activity'] = output[3]
                    condR[exprN + '_Lbnd'] = output[0]
            except:
                print(condR)
                print(affyH)
                print(exprV)
                raise

        return condR


    return conditions.apply(applyF, axis=1)

Igs = {0:'o', 1:'d', 2:'^', 3:'s'}


def PCAplot(axes, dataIn, species):
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    colors = dict(zip(range(5), sns.color_palette()))

    pca = PCA(n_components=4)

    X = dataIn.drop(['avidity', 'ligand', 'IgID'], axis=1)

    X = StandardScaler().fit_transform(X)
    X = pca.fit_transform(X)

    # Move PCs into dataframe
    for ii in range(4):
        dataIn['PC' + str(ii+1)] = X[:, ii]

    for _, row in dataIn.iterrows():
        markerr=Igs[row['IgID']]
        axes[0].errorbar(x=row['PC1'], y=row['PC2'], marker=markerr, ms=3.5)

    loadings = pd.DataFrame(pca.components_, columns=['PC1', 'PC2', 'PC3', 'PC4'])

    loadings.plot(x='PC1', y='PC2', ax=axes[1], kind='scatter')

    axes[0].set_title(species + ' Scores')
    axes[1].set_title(species + ' Loadings')


def PCAmurine(axes, conditions):
    """ Principle Components Analysis of murine FcgR binding predictions """
    from ..StoneModMouse import StoneModelMouse

    affinities = StoneModelMouse().kaMouse
    expressions = {'NK-like':[float('nan'), float('nan'), 4.0, float('nan')], 'DC-like':[3.0, 4.0, 3.0, 3.0]}
    activities = {'DC-like':[1.0, -1.0, 1.0, 1.0]}

    outt = calcActivity(affinities, expressions, conditions, activities)

    PCAplot(axes, outt, 'Murine')


def PCAhuman(axes, conditions):
    from ..StoneModel import StoneModel

    expressions = {'NK-Phe':[float('nan'), float('nan'), float('nan'), float('nan'), 4.0, float('nan')],
                   'NK-Val':[float('nan'), float('nan'), float('nan'), float('nan'), float('nan'), 4.0]}
    activities = {}

    outt = calcActivity(StoneModel().kaBruhns, expressions, conditions, activities)

    PCAplot(axes, outt, 'Human')
