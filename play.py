import numpy as np
import matplotlib.pyplot as plt
##from matplotlib import rc
from StoneModel import StoneModel

## Use LaTex to render text
##rc('text',usetex=True)

## Our data
StoneM1 = StoneModel(False)
StoneM2 = StoneModel(True)

mfiAdjMean1 = StoneM1.mfiAdjMean
mfiAdjMean2 = StoneM2.mfiAdjMean
colors = ['red','blue','green','yellow']
gam = chr(947)
blankLabels = ['']*4

## Relative position of bars, of 9 bars
ind = np.arange(4)
## Width of bars
width = 0.5
## Number of bins per subplot
N = 4

f, axarr = plt.subplots(2,3)
graphs = []
for j in range(6):
    rects = []
    for k in range(4):
        temp = [0]*N
        temp.remove(0)
        temp.insert(k,np.nanmean(mfiAdjMean1[4*(j-1)+k][1:4]))
        rects.append(axarr[int(np.floor(j/3)),j%3].bar(ind,temp,width,color=colors[k]))
##    for k in range(4):
##        temp = [0]*N
##        temp.remove(0)
##        temp.insert(5+k,np.nanmean(mfiAdjMean2[k][5:8]))
##        rects.append(axarr[int(np.floor(j/3)),j%3].bar(ind,temp,width,color=colors[k]))

# axes and labels
for j in range(2):
    for k in range(3):
        axarr[j,k].set_xlim(-0.5*width,len(ind)-1+1.5*width)
        axarr[j,k].set_xticklabels(blankLabels)
        axarr[j,k].grid(b=False)
        axarr[j,k].set_ylim(0,2)
        if k%3 == 0:
            axarr[j,k].set_ylabel('Mean-Adjusted MFIs')
        axarr[j,k].set_title('Fc'+gam+'RIA')
##xTickMarks = ['Group'+str(i) for i in range(1,6)]
##ax.set_xticks(ind+width)
##xtickNames = ax.set_xticklabels(xTickMarks)
##plt.setp(xtickNames, rotation=45, fontsize=10)
##
#### add a legend
leg = axarr[0,0].legend((rects[0][0],rects[1][0]),('Men','Women'),bbox_to_anchor=(1,1))
##
##wm = plt.get_current_fig_manager()
##wm.window.state('zoomed')

##plt.show()
f.savefig('test.png')
