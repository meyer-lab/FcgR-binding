"""
In vivo prediction robustness and first PC's
"""

def makeFigure():
    from .FigureCommon import subplotLabel, getSetup
    from .Figure5 import makeSupp

    # Get list of axis objects
    ax, f = getSetup((7, 4), (2, 3))

    # Make the robustness plot
    robustnessPlot(ax[0])

    # Make the supplemental PCA plots
    makeSupp([ax[1], ax[2], ax[4], ax[5]])

    # Blank out empty spot
    ax[3].axis('off')

    subplotLabel(ax[0], 'A')
    subplotLabel(ax[1], 'B')
    subplotLabel(ax[4], 'C')

    # Tweak layout
    f.tight_layout(w_pad=7)

    return f


def robustnessPlot(ax, calculate=False):
    """ Vary IC concentration and avidity and show the prediction still stands. """
    import os
    import seaborn as sns
    import pandas as pd
    import numpy as np
    from tqdm import tqdm
    from ..StoneModMouseFit import InVivoPredict
    from .FigureCommon import Legend

    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/figS2-robustness.csv")

    if calculate is True:
        # Setup the range of avidity and ligand concentration we'll look at
        gnus = np.logspace(1, 3, 3, base=2, dtype=np.int)
        Los = np.logspace(start=-12, stop=-7, num=30, dtype=np.float)

        pp = pd.DataFrame(np.array(np.meshgrid(gnus, Los)).T.reshape(-1,2), columns=['gnus', 'Los'])

        tqq = tqdm(total=pp.shape[0], desc="Condition calculations")

        def appFun(x):
            x['DPredict'], x['CPredict'], _ = InVivoPredict(x.as_matrix())
            tqq.update()
            return x

        pp = pp.apply(appFun, axis=1)

        tqq.close()

        pp.to_csv(filepath)
    else:
        # Load the data from CSV
        pp = pd.read_csv(filepath, index_col=0)

    avcolors = dict(zip(pp['gnus'].unique(), sns.color_palette()[1:]))

    # Plot the calculated crossvalidation performance
    sns.FacetGrid(pp, hue='gnus', palette=sns.color_palette()[1:]).map(ax.semilogx, 'Los', 'CPredict')

    ax.legend(handles=Legend(avcolors, {}), bbox_to_anchor=(1, 1), loc=2)

    ax.set_xlabel('Assumed IC Conc. (M)')
    ax.set_ylabel('LOO Prediction Explained Var.')
    ax.set_ylim(-1.0, 1.0)
