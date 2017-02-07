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

def seaborn_colorblindGet():
   # This function collects the collor palette settings used in seaborn-colorblind, so as
   # to get all of seaborn's colors without the unwanted formatting effects of seaborn
   # backColor is the background color used in seaborn's colorblind setting
   backColor = (234,234,242)
   backColor = tuple((np.array(backColor)/255).tolist())
   Colors = pd.read_pickle('seaborn_colorblindColors.pkl')
   print(type(Colors))
   print(Colors)
##   Colors = sns.color_palette('colorblind')
##   Colors = sns.color_palette('muted')
   Colors.insert(0,backColor)
   Colors = np.transpose(np.array(Colors))
   Colors = pd.DataFrame(Colors,columns=(['back-color']+['color']*6))
   backColor = (float(Colors[['back-color']].values[j]) for j in range(3))
   colorspre = np.transpose(Colors[['color']].values)
   colors = []
   for j in range(6):
      pre = colorspre[j]
      temp = []
      for k in range(3):
         temp.append(float(pre[k]))
      colors.append(tuple(temp))
   return colors, backColor

colors, backColor = seaborn_colorblindGet()

Igs = {'IgG1':'o', 'IgG2':'d', 'IgG3':'s', 'IgG4':'^'}

fcgrs = ['FcgRI','FcgRIIA-131R','FcgRIIA-131H','FcgRIIB','FcgRIIIA-158F','FcgRIIIA-158V']
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
