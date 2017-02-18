from matplotlib import gridspec
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ..StoneModel import StoneModel
from ..StoneHelper import *
from .FigureCommon import *
import seaborn as sns
import string

def makeFigure():
    # Setup plotting space
    f = plt.figure(figsize=(7,5))

    # Make grid
    gs1 = gridspec.GridSpec(2,3)

    # Get list of axis objects
    ax = [ f.add_subplot(gs1[x]) for x in range(6) ]

    # Plot subplot A
    FirstFigure(ax[0])

    for ii in range(len(ax)):
        subplotLabel(ax[ii], string.ascii_uppercase[ii])

    return f

def FirstFigure(ax = None):
    # If no axis was provided make our own
    if ax == None:
        ax = plt.gca()
