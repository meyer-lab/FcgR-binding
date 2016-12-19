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

def rep(x, N):
  return [item for item in x for i in range(N)]

Igs = {'IgG1':'o', 'IgG2':'d', 'IgG3':'s', 'IgG4':'^'}

FcgRs = {'FcgRI':'black', 'FcgRIIA-Arg':'blue',
          'FcgRIIIA-Phe':'green', 'FcgRIIIA-Val':'red',
          'FcgRIIA-His':'orange', 'FcgRIIB':'gray'}

# Return a dataframe with the measured data labeled with the condition variables
def getMeasuredDataFrame(self):
    normData = pd.DataFrame(self.mfiAdjMean)
    normData = pd.melt(normData, value_name = "Meas")

    normData = (normData.assign(TNP = rep(self.TNPs, 24*4))
                .assign(Ig = self.Igs*12*4)
                .drop('variable', axis = 1)
                .assign(FcgR = rep(self.FcgRs, 4)*8)
                .assign(Expression = rep(np.power(10, self.Rquant), 4)*8)
                .assign(Ka = np.tile(np.reshape(self.kaBruhns, (-1,1)), (8, 1)))
                )

    return normData

# Return a dataframe with the fit data labeled with the condition variables
def getFitPrediction(self, x):
    logSqrErr, outputFit, outputLL, outputRbnd, outputRmulti, outputnXlink, outputLbnd = self.NormalErrorCoef(x, fullOutput = True)

    outputFit = np.reshape(np.transpose(outputFit), (-1, 1))

    dd = (pd.DataFrame(data = outputFit, columns = ['Fit'])
            .assign(LL = np.reshape(np.transpose(outputLL), (-1, 1)))
            .assign(Ig = self.Igs*12)
            .assign(FcgR = rep(self.FcgRs, 4)*2)
            .assign(TNP = rep(self.TNPs, 24))
            .assign(Expression = rep(np.power(10, self.Rquant), 4)*2)
            .assign(Ka = np.tile(np.reshape(self.kaBruhns, (-1,1)), (2, 1)))
            .assign(RbndPred = np.reshape(np.transpose(outputRbnd), (-1, 1)))
            .assign(RmultiPred = np.reshape(np.transpose(outputRmulti), (-1, 1)))
            .assign(nXlinkPred = np.reshape(np.transpose(outputnXlink), (-1, 1)))
            .assign(LbndPred = np.reshape(np.transpose(outputLbnd), (-1, 1)))
            )

    return dd

# Return the fit and measured data merged into a single dataframe
def getFitMeasMerged(self, x):
    fit = getFitPrediction(self, x)
    data = getMeasuredDataFrame(self)

    allFrame = fit.merge(data, 'outer', on=('FcgR', 'TNP', 'Ig', 'Ka', 'Expression'))

    return allFrame

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


def plotL(fitFrame):
    # Massage data frame into mean and sem of measured values
    fitMean = fitFrame.groupby(['Ig', 'TNP', 'FcgR']).mean().reset_index()
    fitSTD = (fitFrame.drop(['Expression', 'Fit', 'LL', 'Ka', 'LbndPred'], axis = 1)
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

                ax.errorbar(temp['LbndPred'], temp['Meas_mean']+0.01,
                            yerr = temp['Meas_std'], marker = Igs[j],
                            mfc = mfcVal, mec = color, ecolor = color,
                            linestyle = 'None')

    patches = list()

    for f in FcgRs:
        patches.append(mpatches.Patch(color=FcgRs[f], label=f))

    for j in Igs:
        patches.append(mlines.Line2D([], [], color='black',
                                     marker=Igs[j], markersize=7, label=j, linestyle='None'))

    #ax.legend(handles=patches)

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.ylabel('Measured Data')
    #ax.set_ylim(0.08, 10)
    #ax.set_xlim(0.08, 10)

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

    cNames = StoneM.pNames
    cNames.insert(0, 'walker')
    cNames.insert(0, 'LL')

    # Read in dataset to Pandas frame
    pdset = pd.DataFrame(dset.value, columns = cNames)

    f.close()

    return (StoneM, pdset)
