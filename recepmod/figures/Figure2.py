from matplotlib import gridspec
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ..StoneModel import StoneModel
from ..StoneHelper import *
from .FigureCommon import *
import os
import seaborn as sns

def makeFigure():
    # Retrieve model and fit from hdf5 file
    M, dset = read_chain(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_chain.h5"))

    pBest = dset.iloc[np.argmax(dset['LL']),:][2:].as_matrix()

    sns.set(style="whitegrid", font_scale=0.7, color_codes=True, palette="colorblind")

    # Setup plotting space
    f = plt.figure(figsize=(7,5))

    # Make grid
    gs1 = gridspec.GridSpec(3,3)
    ax1 = f.add_subplot(gs1[0])

    LLplot(dset, f.add_subplot(gs1[1]))

    ax4 = f.add_subplot(gs1[3])
    ax5 = f.add_subplot(gs1[4])
    ax6 = f.add_subplot(gs1[5])
    ax7 = f.add_subplot(gs1[6])
    ax8 = f.add_subplot(gs1[7])
    ax9 = f.add_subplot(gs1[8])

    plotFit(getFitMeasMergedSummarized(M, pBest), ax = f.add_subplot(gs1[2]))


    histSubplots(dset, axes = [ax4, ax5, ax6, ax7])

    violinPlot(dset, ax = ax8)

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

    objs = sns.violinplot(data=dset,cut=0,ax=ax) # ,color=colors[0]

def LLplot(dset, ax = None):
    if ax == None:
        ax = plt.gca()

    plt.plot(dset['LL'], axes = ax)

def histSubplots(dset, axes=None):
    if axes == None:
        fig, axes = plt.subplots(nrows=1, ncols=4)

    dset[['Kx1']].plot.hist(ax=axes[0], bins = 100, color=colors[0])
    dset[['sigConv1', 'sigConv2']].plot.hist(ax=axes[1], bins = 100, color=[colors[j] for j in range(2)])
    dset[['gnu1', 'gnu2']].plot.hist(ax=axes[2], bins = 100, color=[colors[j] for j in range(2)])
    dset[['sigma', 'sigma2']].plot.hist(ax=axes[3], bins = 100, color=[colors[j] for j in range(2)])

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
    ax.plot([0.08, 10], [0.08, 10])
    ax.set_ylim(0.01, 10)
    ax.set_xlim(0.08, 70)
    plt.xlabel('Fitted prediction')
    plt.ylabel('Measured ligand binding')
