import numpy as np
import matplotlib.pyplot as plt
##from matplotlib import rc
from StoneModel import StoneModel

## Use LaTex to render text
##rc('text',usetex=True)

# Simple data to display in various forms
x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x ** 2)

##fig = plt.figure()
##ax = fig.add_subplot(111)

## Our data
StoneM1 = StoneModel(False)
StoneM2 = StoneModel(True)

mfiAdjMean1 = StoneM1.mfiAdjMean
mfiAdjMean2 = StoneM2.mfiAdjMean
print(mfiAdjMean2)
colors = ['red','blue','green','yellow']
gam = 'γ'

## Relative position of bars, of 9 bars
ind = np.arange(9)
## Width of bars
width = 0.25
## Number of bins per subplot
N = 9

# Four axes, returned as a 2-d array
##f, axarr = plt.subplots(2, 2)
##axarr[0, 0].plot(x, y)
##axarr[0, 0].set_title('Axis [0,0]')
##axarr[0, 1].scatter(x, y)
##axarr[0, 1].set_title('Axis [0,1]')
##axarr[1, 0].plot(x, y ** 2)
##axarr[1, 0].set_title('Axis [1,0]')
##axarr[1, 1].scatter(x, y ** 2)
##axarr[1, 1].set_title('Axis [1,1]')
### Fine-tune figure; hide x ticks for top plots and y ticks for right plots
##plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
##plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)

f, axarr = plt.subplots(2,3)
graphs = []
for j in range(6):
    rects = []
    for k in range(4):
        temp = [0]*N
        temp.remove(0)
        temp.insert(k,np.nanmean(mfiAdjMean1[k][1:4]))
        rects.append(axarr[int(np.floor(j/3)),j%3].bar(ind,temp,width,color=colors[k]))
    for j in range(4):
        temp = [0]*N
        temp.remove(0)
        temp.insert(5+k,np.nanmean(mfiAdjMean2[k][5:8]))
        rects.append(axarr[int(np.floor(j/3)),j%3].bar(ind,temp,width,color=colors[k]))
    
## the bars
##rects1 = ax.bar(ind, menMeans, width,
##                color='black')
##
##rects2 = ax.bar(ind+width, womenMeans, width,
##                    color='red')

# axes and labels
for j in range(2):
    for k in range(3):
        axarr[j,k].set_xlim(-width,len(ind)+width)
        axarr[j,k].set_ylim(0,10)
        axarr[j,k].set_ylabel('Mean-Adjusted MFIs')
        axarr[j,k].set_title('Fc\gammaRIA')
##xTickMarks = ['Group'+str(i) for i in range(1,6)]
##ax.set_xticks(ind+width)
##xtickNames = ax.set_xticklabels(xTickMarks)
##plt.setp(xtickNames, rotation=45, fontsize=10)
##
#### add a legend
##ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )
##
plt.show()
