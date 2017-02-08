import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.colors as mcolors
from matplotlib import rc
from matplotlib.font_manager import FontProperties
#import h5py
#from tqdm import tqdm
##import seaborn as sns

##plt.rc('text',usetex=True)

def seaborn_colorblindGet():
   # This function collects the collor palette settings used in seaborn-colorblind, so as
   # to get all of seaborn's colors without the unwanted formatting effects of seaborn
   # backColor is the background color used in seaborn's colorblind setting
##   Colors = pd.read_pickle('seaborn_colorblindColors.pkl').values
   Colors = pd.read_pickle('seaborn_colorblindColors2.pkl').values
   backColor = tuple([Colors[j][0] for j in range(3)])
   colors = []
   for j in range(1,7):
       colors.append(tuple([Colors[k][j] for k in range(3)]))
   colors2 = []
   for j in range(7,11):
       colors2.append(tuple([Colors[k][j] for k in range(3)]))
   return colors, backColor, colors2

colors, backColor, colors2 = seaborn_colorblindGet()

Igs = {'IgG1':'o', 'IgG2':'d', 'IgG3':'s', 'IgG4':'^'}

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
