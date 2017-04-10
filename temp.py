import recepmod.StoneHelper as sh
import numpy as np
import pandas as pd

M, dset = sh.read_chain('recepmod/data/test_chain.h5')
##M, dset = read_chain(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_chain.h5"))

##dsett = dsett.T.rename(index=[dsett.T[j].loc[['walker']] for j in dsett.T.columns],columns=dsett.T.columns)
##dsett = dsett.T
##
##dsett.columns = [item % 52 for item in dsett.columns]
S, P = sh.geweke_chains(dset)

print
