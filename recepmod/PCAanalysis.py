import os
import numpy as np
import pandas as pd

# Compare across species
path = os.path.dirname(os.path.abspath(__file__))
na = float('nan')

def parallelize_dataframe(df, func):
    """ Calculate the pandas table in parallel. """

    from pathos.multiprocessing import ProcessingPool as Pool
    from multiprocessing import cpu_count
    from tqdm import tqdm

    pool = Pool(cpu_count())

    iterpool = tqdm(pool.imap(func, np.vsplit(df, df.shape[0])), total=df.shape[0])

    return pd.concat(list(iterpool))

def recalcPCA(geno):
    """
    Run the calculations for both the human and murine case under the defined
    conditions.
    """
    from itertools import product

    pd.set_option('expand_frame_repr', False)

    # Setup the table of conditions we'll use.
    avidity = np.logspace(0, 3, 4, base=2, dtype=np.int)
    ligand = np.logspace(start=-9, stop=-9, num=1)
    IgID = np.arange(0, 8, dtype=np.int)
    conditions = pd.DataFrame(list(product(avidity, ligand, IgID)), columns=['avidity', 'ligand', 'IgID'])

    # Run the plot
    PCAall(conditions,geno)


def calcActivity(condR, expressions, affinities, activities):
    """
    Run the activity and binding calculations for the defined condition.
    """
    from .StoneHelper import getMedianKx
    from .StoneNRecep import StoneN
    from .StoneModel import StoneMod

    for exprN, expr in expressions.items():
        # Murine or Human, based on IgID
        which = int(np.floor(condR.IgID / 4))
        
        # Isolate receptors expressed, and keep the index of those
        exprV = np.array(expr[which], dtype=np.float)
        exprIDX = np.logical_not(np.isnan(exprV))
        exprV = exprV[exprIDX]

        # Pull out the relevant affinities from the table
        affyH = affinities[which][exprIDX, int(condR.IgID % 4)]+0.1

        if exprV.size > 1:
            # Setup the StoneN model
            M = StoneN(logR=exprV,
                       Ka=affyH,
                       Kx=getMedianKx(),
                       gnu=np.asscalar(condR.avidity.values),
                       L0=np.asscalar(condR.ligand.values))

            condR[exprN + '_activity'] = M.getActivity(activities[which])
            condR[exprN + '_Lbnd'] = M.getLbnd()
        else:
            output = StoneMod(np.asscalar(exprV),
                              np.asscalar(affyH),
                              np.asscalar(condR.avidity.values),
                              getMedianKx(),
                              np.asscalar(condR.ligand.values),
                              fullOutput=True)

            condR[exprN + '_activity'] = output[3]
            condR[exprN + '_Lbnd'] = output[0]

    return condR

def PCAall(conditions,geno):
    expressions = {}
    expressions["NK"] = [[3.0, 4.0, 3.0, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0]]
    expressions["MO"] = [[3.0, 4.0, 3.0, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0]]
    expressions["DC"] = [[3.0, 4.0, 3.0, 3.0],[3.0, 3.0, nan, 3.0, nan, 4.0, 3.0, nan, 3.0]]
    activities = [[1.0, -1.0, 1.0, 1.0],[1.0, 1.0, -1.0, 1.0, 1.0, 0.0]]

    
    from .StoneModMouse import StoneModelMouse
    affinitiesMur = StoneModelMouse().kaMouse
    affinitiesHum = np.genfromtxt(os.path.join(path, './data/human-affinities.csv'),
                               delimiter=',',
                               skip_header=1,
                               max_rows=9,
                               invalid_raise=True,
                               usecols=list(range(1,5)),
                               dtype=np.float64)
    affinities = [affinitiesMur, affinitiesHum]
    outt = parallelize_dataframe(conditions, lambda x: calcActivity(x, expressions, affinities, activities))

    if geno == 'human-Phe':
        outt.to_csv(os.path.join(path, './data/pca-human-Phe.csv'))
    else:
        outt.to_csv(os.path.join(path, './data/pca-human-Val.csv'))
