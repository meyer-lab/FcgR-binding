"""
In vivo prediction robustness and first PC's
"""
import os
import string
import pandas as pd
import seaborn as sns
import numpy as np
from .FigureCommon import getSetup, Legend, subplotLabel
from ..StoneModMouseFit import InVivoPredict


def makeFigure():
    # Get list of axis objects
    ax, f = getSetup((6, 3), (1, 2))

    # Make FcgR expression plot
    FcgRexpression(ax[0])

    # Make the robustness plot
    robustnessPlot(ax[1])

    # Add subplot labels
    for ii, item in enumerate(ax):
        subplotLabel(item, string.ascii_uppercase[ii])

    # Tweak layout
    f.tight_layout()

    return f


def FcgRexpression(ax):
    """ Calculate robustness or load it. """
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "../data/murine-FcgR-abundance.csv")

    data = pd.melt(pd.read_csv(filepath), id_vars=['Cells'])

    data['Receptor'] = data.variable.str.extract('(R[1234])', expand=False)
    data.drop('variable', inplace=True, axis=1)

    # Setup replacement dict
    FcsIDX = {'R1': r'mFc$\gamma$RI',
              'R2': r'mFc$\gamma$RIIB',
              'R3': r'mFc$\gamma$RIII',
              'R4': r'mFc$\gamma$RIV'}

    # Do replacement for receptors
    data.replace({"Receptor": FcsIDX}, inplace=True)

    sns.factorplot(x="Cells", y="value", hue="Receptor",
                   data=data, kind="bar", ax=ax, ci=63)

    ax.set_ylabel(r'Fc$\gamma$R Expression')
    ax.set_xlabel('')

    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, rotation_mode="anchor", ha="right")


def robustnessPlot(ax):
    """ Vary IC concentration and avidity and show the prediction still stands. """
    # Setup the range of avidity and ligand concentration we'll look at
    gnus = np.logspace(1, 3, 3, base=2, dtype=np.int)
    Los = np.logspace(start=-12, stop=-7, num=30, dtype=np.float)

    pp = pd.DataFrame(np.array(np.meshgrid(gnus, Los)).T.reshape(-1, 2),
                      columns=['gnus', 'Los'])

    pp['CPredict'] = pp.apply(lambda x: InVivoPredict(x.as_matrix())[1], axis=1)

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
