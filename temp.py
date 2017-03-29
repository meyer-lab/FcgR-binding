import recepmod.StoneHelper as sh
import numpy as np

_, dset = sh.read_chain('recepmod/data/test_chain.h5')
##M, dset = read_chain(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_chain.h5"))
print(dset.loc[1.0,:])
