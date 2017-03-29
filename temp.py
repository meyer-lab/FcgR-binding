import numpy as np
import recepmod.StoneHelper as sh
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

a = np.random.rand(100000)
b = np.random.rand(10000)

# Retrieve model and fit from hdf5 file
##M, dset = read_chain(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_chain.h5"))
_, dset = sh.read_chain('recepmod/data/test_chain.h5')

##print(dset.drop(['LL','walker'],1).as_matrix())
##dsett = dset.drop(['LL','walker'],1).as_matrix()
##for j in range(dsett.shape[1]):
##    temp = dsett[:,j]
##    print(sh.geweke(M, dset = read_chain(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_chain.h5"))))

print(sh.geweke_chain(dset))

c, d = ttest_ind(a,b)

for j in range(2,dset.shape[1]):
    plt.figure()
    ax = plt.gca()
    ax.plot(dset.as_matrix()[:,j])
    plt.show()
