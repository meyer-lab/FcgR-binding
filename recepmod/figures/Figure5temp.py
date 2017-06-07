import os
import pandas as pd

# Compare across species

def makeFigure(pcOne='PC 1', pcTwo='PC 2'):
    from .FigureCommon import subplotLabel, getSetup

    path = os.path.dirname(os.path.abspath(__file__))

    # Get list of axis objects
    ax, f = getSetup((7, 5), (2, 2))

    # Run the plots
    PCAplot(ax[0:2],
            pd.read_csv(os.path.join(path, '../data/pca-human-Phe.csv'), index_col=0),
            'Human-Phe', pcOne, pcTwo)
    PCAplot(ax[2:4],
            pd.read_csv(os.path.join(path, '../data/pca-human-Val.csv'), index_col=0),
            'Human-Val', pcOne, pcTwo)

    subplotLabel(ax[0], 'A')
    subplotLabel(ax[2], 'B')

    # Tweak layout
    f.tight_layout(w_pad=12)
        
    return f


def makeSupp(ax):
    x = [j for j in range(10000)]
    ax.plot(x,x)

##    path = os.path.dirname(os.path.abspath(__file__))
##
##    # Run the murine plots
##    PCAplot(ax[0:2],
##            pd.read_csv(os.path.join(path, '../data/pca-murine.csv'), index_col=0),
##            'Murine', 'PC 1', 'PC 2')
##
##    # Run the human plots
##    PCAplot(ax[2:4],
##            pd.read_csv(os.path.join(path, '../data/pca-human.csv'), index_col=0),
##            'Human', 'PC 1', 'PC 2')


def PCAplot(axes, dataIn, species, pcOne='PC 2', pcTwo='PC 3'):
    import numpy as np
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    import seaborn as sns
    from .FigureCommon import Legend

    colors = dict(zip(range(5), sns.color_palette()))
    Igs = {0:'o', 1:'d', 2:'^', 3:'s', 4:'o', 5:'d', 6:'^', 7:'s'}
    fillstyles = {0:'full', 1:'full', 2:'full', 3:'full', 4:'none', 5:'none', 6:'none', 7:'none'}
    quantList = ['Lbnd','activity']
    quantShape = {'Lbnd':'o', 'activity':'d'}

    IgList = ['mIgG1/hIgG1','mIgG2a/hIgG2','mIgG2b/hIgG3','mIgG3/hIgG4']
    Igs = {'mIgG1/hIgG1':'o', 'mIgG2a/hIgG2':'d', 'mIgG2b/hIgG3':'^', 'mIgG3/hIgG4':'s'}

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
        markerr=Igs[int(row['IgID'])]
        avc = 'none' if (row['IgID'] > 3) else avcolors[int(row['avidity'])]
        mec = avcolors[int(row['avidity'])]
        axes[0].errorbar(x=row[pcOne], y=row[pcTwo],
                     markeredgewidth=1, marker=markerr,
                     markeredgecolor=mec, markersize=7,
                     markerfacecolor=avc, ms=5)

    loadings = pd.DataFrame(pca.components_.T, columns=['PC 1', 'PC 2', 'PC 3', 'PC 4'])
    loadings['terms'] = terms
    loadings['cells'], loadings['quantity'] = loadings['terms'].str.split('_', 1).str

    colors = dict(zip(loadings['terms'].unique(), sns.color_palette()))

    for _, row in loadings.iterrows():
        markerr=quantShape[row['quantity']]
        colorr = colors[row['terms']]
        axes[1].errorbar(x=row[pcOne], y=row[pcTwo], marker=markerr, mfc=colorr, ms=5)

    axes[0].set_title(species + ' Scores')
    axes[1].set_title(species + ' Loadings')

    # Ok, now start on legend
##    axes[1].legend(handles=Legend(loadings['cellType'].unique(), colors, quantList, quantShape), bbox_to_anchor=(1, 1), loc=2)
##
##    axes[0].legend(handles=Legend(dataIn['avidity'].unique(), avcolors, IgList, Igs), bbox_to_anchor=(1, 1), loc=2)
##    if species == 'Human-Phe':
##        axes[0].legend(handles=Legend(dataIn['avidity'].unique(), avcolors, hIgList, hIgs), bbox_to_anchor=(1, 1), loc=2)
##    else:
##        axes[0].legend(handles=Legend(dataIn['avidity'].unique(), avcolors, mIgList, mIgs), bbox_to_anchor=(1, 1), loc=2)
    
    # Fix axis limits
    for ii in range(2):
        ylim, xlim = np.max(np.absolute(axes[ii].get_ylim())), np.max(np.absolute(axes[ii].get_xlim()))
        axes[ii].set_ylim(-ylim*1.1, ylim*1.1)
        axes[ii].set_xlim(-xlim*1.1, xlim*1.1)
        axes[ii].set_xlabel(pcOne)
        axes[ii].set_ylabel(pcTwo)
    
