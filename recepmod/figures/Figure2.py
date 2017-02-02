from matplotlib import gridspec
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ..StoneModel import StoneModel
from ..StoneHelper import *
from .FigureCommon import *

def plotQuant(fitMean, nameFieldX, nameFieldY, ax=None, backGray=True, legend=True):
    # This should take a merged and summarized data frame

    if ax == None:
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

                ax.errorbar(temp[nameFieldX], temp[nameFieldY], marker = Igs[j],
                            mfc = mfcVal, mec = color, ecolor = color,
                            linestyle = 'None')

    if legend:
        ax.legend(handles=makeFcIgLegend())

    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.ylabel(nameFieldY)
    plt.xlabel(nameFieldX)
    if backGray:
        ax.set_facecolor(backColor)

def LLscatter(ax=None,backGray=True):
    if ax == None:
        ax = plt.gca()
    dset.plot('LL', 'gnu2', 'scatter',ax=ax)
    if backGray:
        ax.set_facecolor(backColor)
    plt.show()

def gnuScatter(ax=None,backGray=True):
    if ax == None:
        ax = plt.gca()
    dsett.plot(x = 'gnu1', y = 'gnu2', kind = 'scatter', c = 'LL', s = 50,ax=ax)
    plt.xlabel('gnu1')
    if backGray:
        ax.set_facecolor(backColor)
    plt.show()

def violinTest(ax=None):
    if ax == None:
        ax = plt.gca()
    for j in range(len(FcgRs)):
        toplot = np.full(dset[['Rexp']].values.shape,0.0)
        toplot[:][j] = dset[['Rexp']].values[:][j]
        objs = sns.violinplot(data=toplot,color=colors[0],ax=ax)
    ax.set_xticks([])
    ax.semilogy()
    print(objs)
    plt.show()

def sigmaNuHists(axes=None,tight_layout=False,backGray=True):
    if axes == None:
        fig, axes = plt.subplots(nrows=2, ncols=1)
    newdset = dset
    newdset = newdset.assign(sigDiff = lambda x: np.power(10, x.sigConv2 - x.sigConv1))
    newdset = newdset.assign(gnuDiff = lambda x: x.gnu2 / x.gnu1)
    newdset['sigDiff'].plot.hist(ax=axes[0], bins = 100).set_xlabel(r'$\frac{\sigma^*_{26}}{\sigma^*_4}$',fontsize=16)
    newdset['gnuDiff'].plot.hist(ax=axes[1], bins = 20).set_xlabel(r'$\frac{\nu_{26}}{\nu_4}$',fontsize=16)
    if backGray:
        for ax in axes:
            ax.set_facecolor(backColor)
    if tight_layout:
        plt.tight_layout()
    plt.show()

def histSubplots(axes=None,tight_layout=False,backGray=True):
    if axes == None:
        fig, axes = plt.subplots(nrows=3, ncols=2)

    dset[['Kx1'     ]].plot.hist(ax=axes[0,0], bins = 100, color=colors[0])
    dset[['sigConv1', 'sigConv2']].plot.hist(ax=axes[0,1], bins = 100, color=[colors[j] for j in range(2)])
    dset[['gnu1', 'gnu2'        ]].plot.hist(ax=axes[1,0], bins = 100, color=[colors[j] for j in range(2)])
    dset[['sigma', 'sigma2'     ]].plot.hist(ax=axes[1,1], bins = 100, color=[colors[j] for j in range(2)])

    RexpBoxplot(axes[2,0])

##    temp = dset[['Rexp']].values
##    for j in range(temp.shape[1]):
##       y = np.array([-j+5]*temp.shape[0])
##    axes[2,0].set_ylim(0,12000)
##    print(good)
    a = 1e3
    b = 1e5
    c = 1e3
    d = 1e5
##    h, l = axes[2,0].get_legend_handles_labels()
##    h[0].get_bbox().set_points([[a,b],[c,d]])
    ##print(h[0].get_bbox().get_points())

    if tight_layout:
        plt.tight_layout()
    if backGray:
        for elem in axes:
            for ax in elem:
                ax.set_facecolor(backColor)
    plt.show()

#fig = plt.figure((8.5,11))

def RexpBoxplot(ax=None):
    if ax == None:
        ax = plt.gca()
    objs = ax.boxplot(10**dset[['Rexp']].as_matrix(),whis=[5,95],sym='')
    for j in range(int(len(objs['caps'])/2)):
        objs['caps'][2*j].set_color(FcgRs[fcgrs[j]])
        objs['caps'][2*j+1].set_color(FcgRs[fcgrs[j]])
        objs['boxes'][j].set_color(FcgRs[fcgrs[j]])
        objs['medians'][j].set_color(FcgRs[fcgrs[j]])
        objs['whiskers'][2*j].set_color(FcgRs[fcgrs[j]])
        objs['whiskers'][2*j+1].set_color(FcgRs[fcgrs[j]])
        for elem in Rquant[j]:
            ax.plot(j+1,10**elem,color=FcgRs[fcgrs[j]],marker='x')
    ax.semilogy()
    ax.set_xticks([])
    ax.set_ylabel(ylabel='Number of Receptors Expressed')

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
    if backGray:
        ax.set_facecolor(backColor)
