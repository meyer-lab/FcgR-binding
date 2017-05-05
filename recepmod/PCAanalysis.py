import os
import numpy as np
import pandas as pd

# Compare across species
path = os.path.dirname(os.path.abspath(__file__))
na = float('nan')

def parallelize_dataframe(df, func):
    from pathos.multiprocessing import ProcessingPool as Pool
    from multiprocessing import cpu_count
    from tqdm import tqdm

    pool = Pool(cpu_count())

    iterpool = tqdm(pool.imap(func, np.vsplit(df, df.shape[0])), total=df.shape[0])

    return pd.concat(list(iterpool))

def recalcPCA():
    from itertools import product

    pd.set_option('expand_frame_repr', False)

    # Setup the table of conditions we'll use.
    avidity = np.logspace(0, 3, 4, base=2, dtype=np.int)
    ligand = np.logspace(start=-9, stop=-9, num=1)
    IgID = np.arange(0, 4, dtype=np.int)
    conditions = pd.DataFrame(list(product(avidity, ligand, IgID)), columns=['avidity', 'ligand', 'IgID'])

    # Run the murine plots
    PCAmurine(conditions)

    # Run the human plots
    PCAhuman(conditions)


def calcActivity(condR, expressions, affinities, activities):
    from .StoneHelper import getMedianKx
    from .StoneNRecep import StoneN
    from .StoneModel import StoneMod

    for exprN, expr in expressions.items():
        # Isolate receptors expressed, and keep the index of those
        exprV = np.array(expr, dtype=np.float)
        exprIDX = np.logical_not(np.isnan(exprV))
        exprV = exprV[exprIDX]

        # Pull out the relevant affinities from the table
        affyH = affinities[exprIDX, int(condR.IgID)] + 0.1

        if exprV.size > 1:
            # Setup the StoneN model
            M = StoneN(logR=exprV,
                       Ka=affyH,
                       Kx=getMedianKx(),
                       gnu=np.asscalar(condR.avidity.values),
                       L0=np.asscalar(condR.ligand.values))

            condR[exprN + '_activity'] = M.getActivity(activities[exprN])
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


def PCAmurine(conditions):
    """ Principle Components Analysis of murine FcgR binding predictions """
    from .StoneModMouse import StoneModelMouse

    affinities = StoneModelMouse().kaMouse
    expressions = {'NK-like':[na, na, 4.0, na], 'DC-like':[3.0, 4.0, 3.0, 3.0]}
    activities = {'DC-like':[1.0, -1.0, 1.0, 1.0]}

    outt = parallelize_dataframe(conditions, lambda x: calcActivity(x, expressions, affinities, activities))

    outt.to_csv(os.path.join(path, './data/pca-murine.csv'))


def genoComb(begin, vecc):
    """ Builds up all the different genotypes of a single cell type. """

    init = [na] * 9
    outt = {}

    for ii in range(2):
        for jj in range(2):
            for kk in range(2):
                name = begin + '-' + ('HR'[ii]) + ('IT'[jj]) + ('VF'[kk])
                vecCur = vecc.copy()

                vecCur.insert(2-ii, na)
                vecCur.insert(4-jj, na)
                vecCur.insert(7-kk, na)
                outt[name] = vecCur

    return outt


def PCAhuman(conditions):
    from collections import defaultdict
    
    actV = [1, 1, -1, 1, 1, 0]

    affinities = np.genfromtxt(os.path.join(path, './data/human-affinities.csv'),
                        delimiter=',', 
                        skip_header=1,
                        max_rows=9,
                        invalid_raise=True,
                        usecols=list(range(1,5)), 
                        dtype=np.float64)

    expressions = {'NK-Phe': [na,   na,  na,  na,  na,  na, 4.0,  na,  na],
                   'NK-Val': [na,   na,  na,  na,  na,  na,  na, 4.0,  na]}

    expressions.update(genoComb('MO', [3.0, 3.0, 3.0, 4.0, 3.0, 3.0]))
    expressions.update(genoComb('pDC', [2.0, 3.0, 3.0, 2.0, 3.0, 3.0]))

    activities = defaultdict(lambda: actV)

    outt = parallelize_dataframe(conditions, lambda x: calcActivity(x, expressions, affinities, activities))

    outt.to_csv(os.path.join(path, './data/pca-human.csv'))
