from StoneModel import StoneModel
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)

StoneM1 = StoneModel(False)
StoneM2 = StoneModel(True)

mfiAdjMean1 = StoneM1.mfiAdjMean
mfiAdjMean2 = StoneM2.mfiAdjMean

## Relative position of bars, of 9 bars
ind = np.arange(9)
## Width of bars
width = 0.25

tnp4 = [np.nanmean(mfiAdjMean1[j][1:4]) for j in range(4)]
tnp26 = [np.nanmean(mfiAdjMean1[j][5:8]) for j in range(4)]

plt.show()

##rects4 = ax.bar(ind,
