import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import h5py

try:
   import cPickle as pickle
except:
   import pickle

Igs = {'IgG1':'o', 'IgG2':'d', 'IgG3':'s', 'IgG4':'^'}

FcgRs = {'FcgRI':'black', 'FcgRIIA-Arg':'blue',
          'FcgRIIIA-Phe':'green', 'FcgRIIIA-Val':'red',
          'FcgRIIA-His':'orange', 'FcgRIIB':'gray'}

def plotFit(fitFrame):
    # Massage data frame into mean and sem of measured values
    fitMean = fitFrame.groupby(['Ig', 'TNP', 'FcgR']).mean().reset_index()
    fitSTD = (fitFrame.drop(['Expression', 'Fit', 'LL', 'Ka'], axis = 1)
              .groupby(['Ig', 'TNP', 'FcgR']).sem().reset_index())

    fitMean = fitMean.merge(fitSTD, how = 'outer',
                            on = ['Ig', 'TNP', 'FcgR'],
                            suffixes = ['_mean', '_std'])

    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(1, 1, 1)

    for j in Igs:
        for f in FcgRs:
            for x in range(2):
                temp = fitMean[fitMean['Ig'] == j]
                temp = temp[temp['FcgR'] == f]
                color = FcgRs[f]

                if x == 0:
                    temp = temp[temp['TNP'] == 'TNP-4']
                    mfcVal = 'None'
                else:
                    temp = temp[temp['TNP'] != 'TNP-4']
                    mfcVal = color

                ax.errorbar(temp['Fit'], temp['Meas_mean']+0.01,
                            yerr = temp['Meas_std'], marker = Igs[j],
                            mfc = mfcVal, mec = color, ecolor = color,
                            linestyle = 'None')

    patches = list()

    for f in FcgRs:
        patches.append(mpatches.Patch(color=FcgRs[f], label=f))

    for j in Igs:
        patches.append(mlines.Line2D([], [], color='black',
                                     marker=Igs[j], markersize=7, label=j, linestyle='None'))

    ax.legend(handles=patches)

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot([0.08, 10], [0.08, 10])
    ax.set_ylim(0.08, 10)
    ax.set_xlim(0.08, 10)

# Reads in hdf5 file and returns the instance of StoneModel and MCMC chain
def read_chain(filename):
    # Open hdf5 file
    f = h5py.File(filename, 'r')

    # Create pointer to main data set
    dset = f['/data']

    if dset == None:
        raise AssertionError("Dataset from hdf5 was read as empty.")

    # Read in StoneModel and unpickle
    StoneMs = dset.attrs['class']
    StoneM = pickle.loads(StoneMs.tobytes())

    # Read in dataset to Pandas frame
    pdset = pd.DataFrame(dset.value)

    f.close()

    return (StoneM, pdset)
