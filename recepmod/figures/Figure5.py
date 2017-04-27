import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from ..StoneModMouse import StoneModelMouse
from ..StoneModel import StoneModel
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import re

# Compare across species

def makeFigure():
    import string
    from matplotlib import gridspec
    from .FigureCommon import subplotLabel, makeFcIgLegend

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Setup plotting space
    f = plt.figure(figsize=(5, 5))

    # Make grid
    gs1 = gridspec.GridSpec(2,4,width_ratios=[32,11,32,11])

    # Get list of axis objects
    ax = [f.add_subplot(gs1[2*x]) for x in range(4)]

    PCAmurine(ax[0:2])

    PCAhuman(ax[2:4])

    subplotLabel(ax[0], 'A')
    subplotLabel(ax[2], 'B')

    for ii, item in enumerate(ax):
        ax[ii].set_ylabel('PC 2')
        ax[ii].set_xlabel('PC 1')
        # Temporary spacefiller for legend
        ax[ii].legend(handles=makeFcIgLegend(),loc=2,bbox_to_anchor=(1.05,1))

    # Tweak layout
    plt.tight_layout()

    return f

Igs = {'IgG1', 'IgG2a', 'IgG2b', 'IgG3'}
Igidx = dict(zip(Igs, sns.color_palette()))

def PCAmurine(axes):
    """ Principle Components Analysis of FcgR binding predictions """
    # Load murine class
    Mod = StoneModelMouse()
    Mod.v = 20
    Mod.L0 = 1E-9
    table = Mod.pdAvidityTable()
    table['L0'] = Mod.L0

    Mod.L0 = 1E-8
    temp = Mod.pdAvidityTable()
    temp['L0'] = Mod.L0
    table = pd.concat([temp, table])

    Mod.L0 = 1E-7
    temp = Mod.pdAvidityTable()
    temp['L0'] = Mod.L0
    table = pd.concat([temp, table])

    pca = PCA(n_components=5)
    
    scale = StandardScaler()
    
    # remove Req columns
    table = table.select(lambda x: not re.search('Req', x), axis=1)
    table = table.select(lambda x: not re.search('L0', x), axis=1)
    
    # Fit PCA
    result = pca.fit_transform(scale.fit_transform(np.array(table)))
    
    # Assemble scores
    scores = pd.DataFrame(result, index=table.index, columns=['PC1', 'PC2', 'PC3', 'PC4', 'PC5'])
    scores['Avidity'] = scores.apply(lambda x: int(x.name.split('-')[1]), axis=1)
    scores['Ig'] = scores.apply(lambda x: x.name.split('-')[0], axis=1)

    # Assemble loadings
    coefs = pd.DataFrame(pca.components_, index=['PC1', 'PC2', 'PC3', 'PC4', 'PC5'], columns=table.columns).transpose()

    for _, row in scores.iterrows():
        colorr = Igidx[row['Ig']]
        axes[0].errorbar(x=row['PC1'], y=row['PC2'], marker='.', mfc=colorr)

    for _, row in coefs.iterrows():
        axes[1].errorbar(x=row['PC1'], y=row['PC2'], marker='.')

    axes[0].set_title('Murine Scores')
    axes[1].set_title('Murine Loadings')

# Return a dataframe with the fit data labeled with the condition variables
def getFitPrediction(M, x):
    from ..StoneHelper import rep

    _, outputFit, _, outputRbnd, outputRmulti, outputnXlink, outputLbnd, _ = M.NormalErrorCoef(x, fullOutput = True)

    outputFit = np.reshape(np.transpose(outputFit), (-1, 1))

    dd = (pd.DataFrame(data = outputFit, columns = ['Fit'])
          .assign(Ig = M.Igs*12)
          .assign(FcgR = rep(M.FcgRs, 4)*2)
          .assign(TNP = rep(M.TNPs, 24))
          .assign(RbndPred = np.reshape(np.transpose(outputRbnd), (-1, 1)))
          .assign(RmultiPred = np.reshape(np.transpose(outputRmulti), (-1, 1)))
          .assign(nXlinkPred = np.reshape(np.transpose(outputnXlink), (-1, 1)))
          .assign(LbndPred = np.reshape(np.transpose(outputLbnd), (-1, 1)))
         )

    return dd

def PCAhuman(axes):
    Mod = StoneModel()
    from ..StoneHelper import getMedianKx

    x = np.array([5.0, 5.0, 5.0, 5.0, 5.0, 5.0, getMedianKx(), 1, 1, 4, 5, 1, 1], dtype=np.float64)

    #outt = getFitPrediction(Mod, x)


    axes[0].set_title('Human Scores')
    axes[1].set_title('Human Loadings')
