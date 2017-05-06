import numpy as np
import pandas as pd

# Compare across species

def makeFigure(pcOne='PC 2', pcTwo='PC 3'):
    import os
    from .FigureCommon import subplotLabel, getSetup

    path = os.path.dirname(os.path.abspath(__file__))

    # Get list of axis objects
    ax, f = getSetup((7, 5), (2, 2))

    # Run the murine plots
    PCAplot(ax[0:2],
            pd.read_csv(os.path.join(path, '../data/pca-murine.csv'), index_col=0),
            'Murine', pcOne, pcTwo)

    # Run the human plots
    PCAplot(ax[2:4],
            pd.read_csv(os.path.join(path, '../data/pca-human.csv'), index_col=0),
            'Human', pcOne, pcTwo)

    subplotLabel(ax[0], 'A')
    subplotLabel(ax[2], 'B')

    # Tweak layout
    f.tight_layout(w_pad=12)

    return f


def makeSupp():
    return makeFigure(pcOne='PC 1', pcTwo='PC 2')


def PCAplot(axes, dataIn, species, pcOne='PC 2', pcTwo='PC 3'):
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    import seaborn as sns
    from .FigureCommon import Legend

    colors = dict(zip(range(5), sns.color_palette()))
    Igs = {0:'o', 1:'d', 2:'^', 3:'s'}
    mIgs = {'IgG1':'o', 'IgG2a':'d', 'IgG2b':'^', 'IgG3':'s'}
    hIgs = {'IgG1':'o', 'IgG2':'d', 'IgG3':'^', 'IgG4':'s'}
    quantShape = {'Lbnd':'o', 'activity':'d'}

    pca = PCA(n_components=4)

    X = dataIn.drop(['avidity', 'ligand', 'IgID'], axis=1)

    terms = X.columns

    X = pca.fit_transform(StandardScaler().fit_transform(X))

    #print(pca.explained_variance_)

    avcolors = dict(zip(dataIn['avidity'].unique(), sns.color_palette()))

    # Move PCs into dataframe
    for ii in range(4):
        dataIn['PC ' + str(ii+1)] = X[:, ii]

    for _, row in dataIn.iterrows():
        markerr=Igs[row['IgID']]
        avc = avcolors[row['avidity']]
        axes[0].errorbar(x=row[pcOne], y=row[pcTwo], marker=markerr, mfc=avc, ms=5)

    loadings = pd.DataFrame(pca.components_.T, columns=['PC 1', 'PC 2', 'PC 3', 'PC 4'])
    loadings['terms'] = terms
    loadings['cells'], loadings['quantity'] = loadings['terms'].str.split('_', 1).str
    loadings['cellType'], loadings['cellGeno'] = loadings['cells'].str.split('-', 1).str

    colors = dict(zip(loadings['cellType'].unique(), sns.color_palette()))

    for _, row in loadings.iterrows():
        markerr=quantShape[row['quantity']]
        colorr = colors[row['cellType']]
        axes[1].errorbar(x=row[pcOne], y=row[pcTwo], marker=markerr, mfc=colorr, ms=5)

    axes[0].set_title(species + ' Scores')
    axes[1].set_title(species + ' Loadings')

    # Ok, now start on legend
    axes[1].legend(handles=Legend(colors, quantShape), bbox_to_anchor=(1, 1), loc=2)

    if species == 'Human':
        axes[0].legend(handles=Legend(avcolors, hIgs), bbox_to_anchor=(1, 1), loc=2)
    else:
        axes[0].legend(handles=Legend(avcolors, mIgs), bbox_to_anchor=(1, 1), loc=2)

    # Fix axis limits
    for ii in range(2):
        ylim, xlim = np.max(np.absolute(axes[ii].get_ylim())), np.max(np.absolute(axes[ii].get_xlim()))
        axes[ii].set_ylim(-ylim*1.1, ylim*1.1)
        axes[ii].set_xlim(-xlim*1.1, xlim*1.1)
        axes[ii].set_xlabel(pcOne)
        axes[ii].set_ylabel(pcTwo)
