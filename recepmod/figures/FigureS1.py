import seaborn as sns
from .FigureCommon import FcgRidx, subplotLabel, getSetup


def makeFigure():
    from ..StoneHelper import read_chain, mapMCMC, getFitPrediction

    # Get list of axis objects
    ax, f = getSetup((7, 6), (4, 3))

    # Retrieve model and fit from hdf5 file
    M, dset = read_chain()

    dsetSamp = dset.sample(40)

    runFunc = lambda x: getFitPrediction(M, x[2:])

    output = mapMCMC(runFunc, dsetSamp, quiet=True)

    subplotLabel(ax[0], 'A')
    subplotLabel(ax[6], 'B')

    # Bound / total receptor prediction
    Rbndplot(output.copy(), axarr = ax[0:])

    # Multimerized receptor prediction
    Rmultiplot(output.copy(), axarr = ax[6:])

    # Tweak layout
    f.tight_layout()

    return f

def Rbndplot(output, axarr):
    output['RbndPred'] = output.apply(lambda row: (row['RbndPred'] / (row['RbndPred'] + row['Req'])), axis=1)

    fcIter = zip(axarr, FcgRidx.keys())

    # Loop through receptors creating plot
    for axx, fcr in fcIter:
        sns.boxplot(x="Ig",
                    y = 'RbndPred',
                    hue="TNP",
                    data=output.loc[output['FcgR'] == fcr,:],
                    ax = axx,
                    showfliers=False)

        axx.set_ylabel(r'Fc$\gamma$R bound/total')
        axx.set_xlabel("")
        axx.set_ylim((0, 1))
        axx.legend_.remove()
        axx.set_title(fcr.replace('FcgR', r'Fc$\gamma$R'))

def Rmultiplot(output, axarr):
    output['RmultiPred'] = output.groupby(['pSetNum'])['RmultiPred'].apply(lambda x: x / x.mean())
    output['nXlinkPred'] = output.groupby(['pSetNum'])['nXlinkPred'].apply(lambda x: x / x.mean())

    fcIter = zip(axarr, FcgRidx.keys())

    # Loop through receptors creating plot
    for axx, fcr in fcIter:
        sns.boxplot(x="Ig",
                    y = "nXlinkPred",
                    hue="TNP",
                    data=output.loc[output['FcgR'] == fcr,:],
                    ax = axx)

        axx.set_ylabel(r'Multimerized Fc$\gamma$R')
        axx.set_xlabel("")
        axx.set_ylim((0, axx.get_ylim()[1]))
        axx.legend_.remove()
        axx.set_title(fcr.replace('FcgR', r'Fc$\gamma$R'))
