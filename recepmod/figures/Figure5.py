import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from ..StoneModMouse import StoneModelMouse

# Compare across species

def makeFigure():
    import string
    from matplotlib import gridspec
    from ..StoneHelper import getMedianKx
    from .FigureCommon import subplotLabel

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Load murine class
    Mod = StoneModelMouse()

    # Setup plotting space
    f = plt.figure(figsize=(5, 5))

    # Make grid
    gs1 = gridspec.GridSpec(2, 2)

    # Get list of axis objects
    ax = [ f.add_subplot(gs1[x]) for x in range(4) ]

    for ii, item in enumerate(ax):
        subplotLabel(item, string.ascii_uppercase[ii])

    # Tweak layout
    plt.tight_layout()

    return f