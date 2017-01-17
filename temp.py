import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
##############DELETE!!!!!!!####################
from StoneModel import StoneModel
Rquant = StoneModel(True).Rquant

rc('text',usetex=False)

N = len(Rquant)
width = 0.5
iterable = [(np.nanmean(10**Rquant[j]),np.nanstd(10**Rquant[j])) for j in range(N)]

ind = np.arange(N)
colors = ['red','orange','yellow','green','blue','purple']
species = ['IA','IIA-131R','IIA-131H','IIB','IIIA-158F','IIIA-158V']

f = plt.figure()
ax = f.add_subplot(121)
rects = []
for j in range(N):
    temp = [0]*(N-1)
    temp.insert(j,iterable[j][0])
    stds = [0]*(N-1)
    stds.insert(j,iterable[j][1])
    rects.append(ax.bar(ind,temp,color=colors[j],yerr=stds,error_kw=dict(elinewidth=2,ecolor='black')))

ax.xaxis.set_visible(False)
ax.set_xlim(-0.5*width,len(ind)+0.2*width)
ax.tick_params(axis='x',length=0)
ax.grid(b=False)
##ax.set_ylim(0,7)
ax.set_yscale('log')
f.suptitle('Receptor Quantification by Species',fontsize=18)

leg = ax.legend((rects[j][0] for j in range(N)),(r'Fc$\gamma$R'+species[j] for j in range(N)),bbox_to_anchor=(2,1))
plt.show()
