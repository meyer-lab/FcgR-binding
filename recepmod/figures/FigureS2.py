"""
In vivo prediction robustness and first PC's
"""


def makeFigure():
    from .FigureCommon import getSetup

    # Get list of axis objects
    ax, f = getSetup((2, 2), (1, 1))

    # Make the robustness plot
    robustnessPlot(ax[0])

    # Tweak layout
    f.tight_layout()

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

    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "../data/figS2-robustness.csv")

    if calculate is True:
        # Setup the range of avidity and ligand concentration we'll look at
        gnus = np.logspace(1, 3, 3, base=2, dtype=np.int)
        Los = np.logspace(start=-12, stop=-7, num=30, dtype=np.float)

        pp = pd.DataFrame(np.array(np.meshgrid(gnus, Los)).T.reshape(-1, 2),
                          columns=['gnus', 'Los'])

        tqdm.pandas(desc="Condition calculations")

        pp['CPredict'] = pp.progress_apply(lambda x: InVivoPredict(x.as_matrix())[1], axis=1)

        pp.to_csv(filepath)
    else:
        # Load the data from CSV
        pp = pd.read_csv(filepath, index_col=0)

    # Change avidities to strings
    pp['gnus'] = pp['gnus'].apply(lambda gnu: r'$\nu=' + str(int(gnu)) + '$')

    avcolors = dict(zip(pp['gnus'].unique(), sns.color_palette()[1:]))

    # Plot the calculated crossvalidation performance
    sns.FacetGrid(pp,
                  hue='gnus',
                  palette=sns.color_palette()[1:]).map(ax.semilogx, 'Los', 'CPredict')

    ax.legend(handles=Legend(pp['gnus'].unique(), avcolors, [], {}), bbox_to_anchor=(1, 1), loc=2)

    ax.set_xlabel('Assumed IC Conc. (M)')
    ax.set_ylabel('LOO Prediction R-Squared')
    ax.set_ylim(0.0, 1.0)
