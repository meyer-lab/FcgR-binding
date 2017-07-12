"""
Make a supplemental figure with the autocorrelation analysis.
"""

def makeFigure():
    from ..StoneHelper import read_chain
    from .FigureCommon import getSetup

    # Get list of axis objects
    ax, f = getSetup((7, 6), (3, 5))

    # Retrieve model and fit from hdf5 file
    _, dset = read_chain()

    d = {'Rexp': [r'Fc$\gamma$RIA', r'Fc$\gamma$RIIA-131R',
                  r'Fc$\gamma$RIIA-131H', r'Fc$\gamma$RIIB',
                  r'Fc$\gamma$RIIIA-158F', r'Fc$\gamma$RIIIA-158V']}

    # Rename the receptor expression columns
    dset = dset.rename(columns=lambda c: d[c].pop(0) if c in d.keys() else c)

    # Make the row something we can refer to
    dset['row'] = dset.index

    # Make a column for which step this came from within the walker
    dset['Step'] = dset.groupby('walker')['row'].rank()

    # Find the variables we want to run this on
    params = dset.columns.drop(['Step', 'walker', 'row', 'LL'])

    # Run the autocorrelation plotting on each variable
    for ii, item in enumerate(params):
        plotAutoC(ax[ii], dset, item)
        ax[ii].set_ylabel('Autocorrelation')
    ax[13].set_axis_off()
    ax[14].set_axis_off()

    # Tweak layout
    f.tight_layout()

    return f


def plotAutoC(ax, dset, coll):
    from .FigureCommon import texRename
    """
    Run the autocorrelation analysis and plot for the selected variable.
    """
    from statsmodels.tsa.stattools import acf
    import numpy as np

    # Pivot to separate out all the walkers
    dd = dset.pivot(index='Step', columns='walker', values=coll)

    # Calculate the autocorrelation
    outt = dd.apply(lambda x: acf(x, nlags=x.size))

    # Plot the values
    outt.plot(ax=ax, legend=False, linewidth=0.5)

    # Rename columns for plotting
    coll = texRename(coll)
    ax.set_title(coll)

    # Indicate the confidence intervals for failure
    z95 = 1.959963984540054 / np.sqrt(outt.shape[0])
    z99 = 2.5758293035489004 / np.sqrt(outt.shape[0])
    ax.axhline(y=z99, linestyle='--', color='grey', linewidth=0.5)
    ax.axhline(y=z95, color='grey', linewidth=0.5)
    ax.axhline(y=0.0, color='black', linewidth=0.5)
    ax.axhline(y=-z95, color='grey', linewidth=0.5)
    ax.axhline(y=-z99, linestyle='--', color='grey', linewidth=0.5)

