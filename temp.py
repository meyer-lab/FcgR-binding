import matplotlib.pyplot as plt
from StoneModel import StoneModel
from StoneHelper import *
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
import numpy as np

StoneM = StoneModel()

f = plt.figure(figsize=(20,20))
gs1 = gridspec.GridSpec(2,2,height_ratios=[1,3],width_ratios=[1,3])
ax = f.add_subplot(gs1[0])
FcgRQuantificationFigureMaker(StoneM,ax,legbbox=(1.75,1),titlefontsize=16)
gs2 = gridspec.GridSpec(8,4,height_ratios=[1,1,1,1,1,4,1,4])
axarr = []
for j in range(6):
    axarr.append(f.add_subplot(gs2[20+j+5*int(np.floor(j/3))]))
mfiAdjMeanFigureMaker(StoneM,axarr,legbbox=(1.5,1),tnpbsafontsize=12)
##plt.show()

with PdfPages('test.pdf') as pdf:
    pdf.savefig(f)
