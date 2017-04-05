import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Figure 5: Predict in vivo response

def makeFigure():
    print("Starting Figure 5")

    import string
    import os
    from matplotlib import gridspec
    from ..StoneHelper import read_chain
    from .FigureCommon import subplotLabel

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Retrieve model and fit from hdf5 file
    _, dset = read_chain(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_chain.h5"))

    # Only keep good samples
    dsetFilter = dset.loc[dset['LL'] > (np.max(dset['LL'] - 4)),:]
    Kx = np.power(10, np.median(dsetFilter['Kx1']))

    # Setup plotting space
    f = plt.figure(figsize=(7,5))

    # Make grid
    gs1 = gridspec.GridSpec(2,3)

    # Get list of axis objects
    ax = [ f.add_subplot(gs1[x]) for x in range(6) ]

    for ii, item in enumerate(ax):
        subplotLabel(item, string.ascii_uppercase[ii])

    # Tweak layout
    plt.tight_layout()

    return f
