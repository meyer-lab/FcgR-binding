from recepmod.figures.Figure5 import PCAmurine
import matplotlib.pyplot as plt
from matplotlib import gridspec

f = plt.figure(figsize=(5,5))
gs = gridspec.GridSpec(1,2)
axx = []
for j in range(2):
    axx.append(f.add_subplot(gs[j]))
PCAmurine(axx)
plt.show()
