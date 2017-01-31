import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
import numpy as np
import sys

sys.path.append('../')

import StoneModel
from StoneHelper import *

StoneM = StoneModel.StoneModel()

f = plt.figure(figsize=(8.5,11))
gs1 = gridspec.GridSpec(2,3,height_ratios=[1,3],width_ratios=[2,3,3])
ax = f.add_subplot(gs1[0])
FcgRQuantificationFigureMaker(StoneM,ax,legbbox=(1.75,1),titlefontsize=16)
ax2 = f.add_subplot(gs1[1])
ax3 = f.add_subplot(gs1[2])
plotNormalizedBindingvsKA(ax2, ax3)
gs2 = gridspec.GridSpec(8,4,height_ratios=[1,1,1,1,1,4,1,4])
axarr = []
for j in range(6):
    axarr.append(f.add_subplot(gs2[20+j+5*int(np.floor(j/3))]))
mfiAdjMeanFigureMaker(StoneM,axarr,legbbox=(1.5,1),tnpbsafontsize=12)
plt.show()

##with PdfPages('fig1test.pdf') as pdf:
##    pdf.savefig(f)
