from matplotlib import gridspec
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ..StoneModel import StoneModel
from ..StoneHelper import *
from .FigureCommon import *
import seaborn as sns

def makeFigure():
    # Setup plotting space
    f = plt.figure(figsize=(7,5))

    # Make grid
    gs1 = gridspec.GridSpec(2,3)
    ax1 = f.add_subplot(gs1[0])
    ax2 = f.add_subplot(gs1[1])
    ax3 = f.add_subplot(gs1[2])
    ax4 = f.add_subplot(gs1[3])
    ax5 = f.add_subplot(gs1[4])
    ax6 = f.add_subplot(gs1[5])

    return f
