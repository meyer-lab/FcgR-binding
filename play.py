import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from StoneModel import StoneModel

def mfiAdjMeanFigureMaker(newdata=True):
    ## Use LaTex to render text; though usetex is input as False, it causes LaTex to be used.
    ## Inputting usetex = True causes an error; this is a bug I found online
    ## (http://matplotlib.1069221.n5.nabble.com/tk-pylab-and-unicode-td10458.html)
    rc('text',usetex=False)

    ## Our data
    StoneM = StoneModel(newdata)
    mfiAdjMean = StoneM.mfiAdjMean

    ## Number of bars, including an "empty" bar between TNP-4-BSA and TNP-26-BSA data
    N = 9

    ## Setting up strings useful for plotting
    colors = ['red','blue','green','yellow']
    species = []
    species.append(r'Fc$\gamma$RIA')
    species.append(r'Fc$\gamma$RIIA-131R')
    species.append(r'Fc$\gamma$RIIA-131H')
    species.append(r'Fc$\gamma$RIIB')
    species.append(r'Fc$\gamma$RIIIA-158F')
    species.append(r'Fc$\gamma$RIIIA-158V')
    blankLabels = ['']*N

    ind = np.arange(N)
    ## Width of bars
    width = 0.5

    ## Generate a figure with a 2 X 4 array of subplots; the rightmost column exists
    ## only as a place to put the legend. The axes of these rightmost plots are whited
    ## out for de-facto invisibility.
    f, axarr = plt.subplots(2,4,figsize = (14,15))

    ## Plotting mfiAdjMean
    for j in range(6):
        rects = []
        for k in range(4):
            temp = [0]*N
            temp.remove(0)
            temp.insert(k,np.nanmean(mfiAdjMean[4*(j-1)+k][1:4]))
            rects.append(axarr[int(np.floor(j/3)),int(j+np.floor(j/3))%4].bar(ind,temp,width,color=colors[k]))
        
        for k in range(4):
            temp = [0]*N
            temp.remove(0)
            temp.insert(5+k,np.nanmean(mfiAdjMean[4*(j-1)+k][5:8]))
            rects.append(axarr[int(np.floor(j/3)),int(j+np.floor(j/3))%4].bar(ind,temp,width,color=colors[k]))

    # axes and labels
    for j in range(2):
        for k in range(3):
            axarr[j,k].set_xlim(-0.5*width,len(ind)-1+1.5*width)
            axarr[j,k].set_xticklabels(blankLabels)
            axarr[j,k].grid(b=False)
            axarr[j,k].set_ylim(0,5)
            if k%3 == 0:
                axarr[j,k].set_ylabel('maMFIs',fontsize=14)
            axarr[j,k].set_title(species[3*j+k],fontsize=16)

    ## Add a legend denoting IgG species
    leg = axarr[0,3].legend((rects[i][0] for i in range(4)),('IgG'+str(i+1) for i in range(4)),bbox_to_anchor=(0.5,1))
    ## White out the rightmost set of aubplots
    for j in range(2):
        axarr[j,3].spines['bottom'].set_color('white')
        axarr[j,3].spines['top'].set_color('white') 
        axarr[j,3].spines['right'].set_color('white')
        axarr[j,3].spines['left'].set_color('white')
        axarr[j,3].tick_params(axis='x', colors='white')
        axarr[j,3].tick_params(axis='y', colors='white')

    ## Set title for the set of plots
    ##titleEnd = ' (New Data)'
    f.suptitle('Mean-Adjusted MFIs (Original Data)',fontsize=18)
    ## Show figure
    plt.show()
    ## Save figure as image
    f.savefig('mfiAdjMean1.png')

mfiAdjMeanFigureMaker(False)
