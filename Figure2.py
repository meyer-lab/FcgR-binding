import matplotlib.pyplot as plt
from StoneModel import StoneModel
from StoneHelper import *
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec
import numpy as np
from matplotlib import rc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import importlib
import StoneHelper
import StoneModel
import seaborn as sns

rc('text',usetex=False)

importlib.reload(StoneHelper)
importlib.reload(StoneModel)

Rquant = StoneModel.StoneModel().Rquant

M, dset = StoneHelper.read_chain("mcmc_chain.h5")

bestIDX = np.argmax(dset['LL'])

p = dset.iloc[bestIDX,:][2:].as_matrix()

# Trim the burn in period
dset = dset.iloc[300::,:]

##print(dset.columns)

fig, axes = plt.subplots(nrows=3, ncols=2)
colors = ['red','orange','yellow','green','blue','purple']

dset[['Kx1'     ]].plot.hist(ax=axes[0,0], bins = 100)
dset[['sigConv1', 'sigConv2']].plot.hist(ax=axes[0,1], bins = 100)
dset[['gnu1', 'gnu2'        ]].plot.hist(ax=axes[1,0], bins = 100)
dset[['sigma', 'sigma2'     ]].plot.hist(ax=axes[1,1], bins = 100)
##for j in range(len(colors)):
##    fcgr = Rquant[j]
##    for meas in fcgr:
##        axes[2,0].plot(np.repeat(meas,dset.shape[0]),np.arange(0,dset.shape[0]),color=colors[j])
dset[['Rexp'   ]].plot.hist(ax=axes[2,0], bins = 30,color=colors, alpha=0.25)
temp = dset[['Rexp']].values
##print(temp)
##g, axes = plt.subplots(nrows=3, ncols=2)
##for j in range(3):
##    for k in range(2):
##        axes[j,k].hist(bins=30, 
axes[2,0].set_ylim(0,12000)
a = 1e3
b = 1e5
c = 1e3
d = 1e5
h, l = axes[2,0].get_legend_handles_labels()
h[0].get_bbox().set_points([[a,b],[c,d]])
##print(h[0].get_bbox().get_points())
axes[2,1].set_axis_off()

plt.tight_layout()
plt.gcf().show()

dset = dset.assign(sigDiff = lambda x: np.power(10, x.sigConv2 - x.sigConv1))
dset = dset.assign(gnuDiff = lambda x: x.gnu2 / x.gnu1)

fig, axes = plt.subplots(nrows=2, ncols=1)

dset['sigDiff'].plot.hist(ax=axes[0], bins = 100).set_xlabel(r'$\frac{\sigma^*_{26}}{\sigma^*_4}$',fontsize=16)
dset['gnuDiff'].plot.hist(ax=axes[1], bins = 20).set_xlabel(r'$\frac{\nu_{26}}{\nu_4}$',fontsize=16)

plt.tight_layout()
##plt.gcf().show()

dset.plot('LL', 'gnu2', 'scatter')
##plt.gcf().show()

dsett = dset.sort_values(by = 'LL')

dsett.plot(x = 'gnu1', y = 'gnu2', kind = 'scatter', c = 'LL', s = 50)
#plt.xlabel('gnu1')
##plt.gcf().show()
