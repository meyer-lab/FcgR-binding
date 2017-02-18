import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.colors as mcolors
from matplotlib import rc
from matplotlib.font_manager import FontProperties

Igs = {'IgG1':'o', 'IgG2':'d', 'IgG3':'s', 'IgG4':'^'}
colors = ['r', 'g', 'b', 'y', 'k', 'm']

fcgrs = [r'Fc$\gamma$RI',r'Fc$\gamma$RIIA-131R',r'Fc$\gamma$RIIA-131H',r'Fc$\gamma$RIIB',r'Fc$\gamma$RIIIA-158F',r'Fc$\gamma$RIIIA-158V']
FcgRs = {}
for j in range(len(fcgrs)):
    FcgRs[fcgrs[j]] = colors[j]
igs = [elem for elem in Igs]
fcgrs = [elem for elem in FcgRs]

def makeFcIgLegend():
    patches = list()

    for f in FcgRs:
        patches.append(mpatches.Patch(color=FcgRs[f], label=f))

    for j in Igs:
        patches.append(mlines.Line2D([], [], color='black', marker=Igs[j], markersize=7, label=j, linestyle='None'))

    return patches

def subplotLabel(ax, letter):
    ax.text(-0.1, 1.1, letter, transform=ax.transAxes, fontsize=16, fontweight='bold', va='top')
