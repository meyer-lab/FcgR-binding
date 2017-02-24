from matplotlib import gridspec, rcParams
import numpy as np
import matplotlib.pyplot as plt
import os
import seaborn as sns
import string
from ..StoneHelper import read_chain, getFitMeasMergedSummarized
from .FigureCommon import Igs, FcgRs, igs, fcgrs, makeFcIgLegend, colors, subplotLabel

def makeFigure():
    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Retrieve model and fit from hdf5 file
    M, dset = read_chain(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_chain.h5"))

    pBest = dset.iloc[np.argmax(dset['LL']),:][2:].as_matrix()

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")
    rcParams['lines.markeredgewidth'] = 1.0

    # Setup plotting space
    f = plt.figure(figsize=(7,5))

    # Make grid
    gs1 = gridspec.GridSpec(3,3)

    # Get list of axis objects
    ax = [ f.add_subplot(gs1[x]) for x in range(9) ]

    # Place likelihood plot
    LLplot(dset, ax[1])

    # Show predicted versus actual
    plotFit(getFitMeasMergedSummarized(M, pBest), ax = ax[2])

    # Make histogram subplots
    histSubplots(dset, axes = [ax[3], ax[4], ax[5], ax[6]])

    violinPlot(dset, ax = ax[7])

    for ii in range(len(ax)):
        subplotLabel(ax[ii], string.ascii_uppercase[ii])

    return f

def plotQuant(fitMean, nameFieldX, nameFieldY, ax=None, backGray=True, legend=True):
    # This should take a merged and summarized data frame

    if ax == None:
        fig = plt.figure(figsize=(7,6))
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

                ax.errorbar(temp[nameFieldX], temp[nameFieldY], marker = Igs[j],
                            mfc = mfcVal, mec = color, ecolor = color,
                            linestyle = 'None')

    if legend:
        ax.legend(handles=makeFcIgLegend())

    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.ylabel(nameFieldY)
    plt.xlabel(nameFieldX)

def violinPlot(dset, ax=None):
    # If no axis was provided make our own
    if ax == None:
        ax = plt.gca()

    dset = dset[['Rexp']]
    dset.columns = fcgrs

    objs = sns.violinplot(data=dset,cut=0,ax=ax)

    ax.set_xticklabels(ax.get_xticklabels(),
                       rotation=40,
                       rotation_mode="anchor",
                       ha="right")

def LLplot(dset, ax = None):
    # TODO: Should this maybe be a plot of the autocorrelation or geweke criterion instead?
    if ax == None:
        ax = plt.gca()

    # Find out how many walkers we had
    nwalkers = int(np.max(dset['walker'])) + 1

    # Make an index for what step values came from
    dset = dset.assign(IDX = np.repeat(range(int(dset.shape[0]/nwalkers)), nwalkers))

    # Reorganize data for plotting
    dset = dset[['LL', 'walker', 'IDX']].pivot(index = 'IDX', columns = 'walker', values = 'LL')

    # Plot LL values
    dset.plot(ax = ax, legend = False, ylim = (-100, -50))

    # Try and fix overlapping elements
    plt.tight_layout()


def histSubplots(dset, axes=None):
    if axes == None:
        fig, axes = plt.subplots(nrows=1, ncols=4)

    dsetFilter = dset.loc[dset['LL'] > (np.max(dset['LL'] - 10)),:]

    dsetFilter[['Kx1']].plot.hist(ax=axes[0], bins = 100, color=colors[0])
    dsetFilter[['sigConv1', 'sigConv2']].plot.hist(ax=axes[1], bins = 100, color=[colors[j] for j in range(2)])
    dsetFilter[['gnu1', 'gnu2']].plot.hist(ax=axes[2], bins = 100, color=[colors[j] for j in range(2)])
    dsetFilter[['sigma', 'sigma2']].plot.hist(ax=axes[3], bins = 100, color=[colors[j] for j in range(2)])

def plotFit(fitMean,ax=None, backGray=True):
    # This should take a merged and summarized data frame
    fitMeanPre = fitMean[['Fit','Meas_mean','Meas_std']].as_matrix()
    if ax == None:
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(1, 1, 1)

    for j in range(len(Igs)):
        for k in range(len(FcgRs)):
            for l in range(2):
                if l == 0:
                    mfcVal = 'None'
                else:
                    mfcVal = FcgRs[fcgrs[k]]
                ax.errorbar(fitMeanPre[8*j+k+4*l][0],fitMeanPre[8*j+k+4*l][1]+0.01,yerr=fitMeanPre[8*j+k+4*l][2],marker=Igs[igs[j]],mfc=mfcVal,mec=FcgRs[fcgrs[k]],ecolor=FcgRs[fcgrs[k]],linestyle='None')

    ax.legend(handles=makeFcIgLegend(), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot([0.01, 10], [0.01, 10])
    ax.set_ylim(0.01, 10)
    ax.set_xlim(0.01, 10)
    plt.xlabel('Fitted prediction')
    plt.ylabel('Measured ligand binding')
