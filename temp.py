import matplotlib.pyplot as plt
from StoneModel import StoneModel
from StoneHelper import *
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

StoneM = StoneModel()

f = plt.figure(figsize=(20,20))
ax = f.add_subplot(221)
FcgRQuantificationFigureMaker(StoneM,ax)
axarr = []
for j in range(6):
    exec('axarr.append(f.add_subplot(8,4,'+str(int(25+j+np.floor(j/3)))+'))')
mfiAdjMeanFigureMaker(StoneM,axarr)
##plt.show()

with PdfPages('test.pdf') as pdf:
    pdf.savefig(f)
