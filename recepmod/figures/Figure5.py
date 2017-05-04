import os
import matplotlib
matplotlib.use('AGG')
import numpy as np
import pandas as pd
import seaborn as sns

# Compare across species
path = os.path.dirname(os.path.abspath(__file__))

def makeFigure():
    import string
    from matplotlib import gridspec
    import matplotlib.pyplot as plt
    from .FigureCommon import subplotLabel

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Setup plotting space
    f = plt.figure(figsize=(7, 5))

    # Make grid
    gs1 = gridspec.GridSpec(2, 4, width_ratios=[32, 11, 32, 11])

    # Get list of axis objects
    ax = [f.add_subplot(gs1[2*x]) for x in range(4)]

    # Run the murine plots
    PCAplot(ax[0:2],
            pd.read_csv(os.path.join(path, '../data/pca-murine.csv'), index_col=0),
            'Murine')

    # Run the human plots
    PCAplot(ax[2:4],
            pd.read_csv(os.path.join(path, '../data/pca-human.csv'), index_col=0),
            'Human')

    subplotLabel(ax[0], 'A')
    subplotLabel(ax[2], 'B')

    for ii, item in enumerate(ax):
        ax[ii].set_ylabel('PC 2')
        ax[ii].set_xlabel('PC 1')

    # Tweak layout
    f.tight_layout()

    return f

Igs = {0:'o', 1:'d', 2:'^', 3:'s'}
mIgs = {'IgG1':'o', 'IgG2a':'d', 'IgG2b':'^', 'IgG3':'s'}
hIgs = {'IgG1':'o', 'IgG2':'d', 'IgG3':'^', 'IgG4':'s'}
quantShape = {'Lbnd':'o', 'activity':'d'}


def Legend(ax, colors, shapes):
    """ Make legend. """
    import matplotlib.lines as mlines
    import matplotlib.patches as mpatches

    patches = list()

    for key, val in colors.items():
        patches.append(mpatches.Patch(color=val, label=key))

    for key, val in shapes.items():
        patches.append(mlines.Line2D([], [], color='black', marker=val, markersize=7, label=key, linestyle='None'))
    
    ax.legend(handles=patches, bbox_to_anchor=(1, 1), loc=2)


def PCAplot(axes, dataIn, species):
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    colors = dict(zip(range(5), sns.color_palette()))

    pca = PCA(n_components=4)

    X = dataIn.drop(['avidity', 'ligand', 'IgID'], axis=1)

    terms = X.columns

    X = pca.fit_transform(StandardScaler().fit_transform(X))

    print(pca.explained_variance_)

    avcolors = dict(zip(dataIn['avidity'].unique(), sns.color_palette()))

    # Move PCs into dataframe
    for ii in range(4):
        dataIn['PC' + str(ii+1)] = X[:, ii]

    for _, row in dataIn.iterrows():
        markerr=Igs[row['IgID']]
        avc = avcolors[row['avidity']]
        axes[0].errorbar(x=row['PC1'], y=row['PC2'], marker=markerr, mfc=avc, ms=3.5)

    loadings = pd.DataFrame(pca.components_.T, columns=['PC1', 'PC2', 'PC3', 'PC4'])
    loadings['terms'] = terms
    loadings['cells'], loadings['quantity'] = loadings['terms'].str.split('_', 1).str

    colors = dict(zip(loadings['cells'].unique(), sns.color_palette()))

    for _, row in loadings.iterrows():
        markerr=quantShape[row['quantity']]
        colorr = colors[row['cells']]
        axes[1].errorbar(x=row['PC1'], y=row['PC2'], marker=markerr, mfc=colorr, ms=5)

    axes[0].set_title(species + ' Scores')
    axes[1].set_title(species + ' Loadings')

    # Ok, now start on legend
    Legend(axes[1], colors, quantShape)

    if species == 'Human':
        Legend(axes[0], avcolors, hIgs)
    else:
        Legend(axes[0], avcolors, mIgs)
