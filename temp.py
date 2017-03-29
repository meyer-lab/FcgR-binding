import numpy as np
from pymc3 import Model, Normal
from pymc3.diagnostics import geweke
a = np.random.normal(size=(1,10000))

mod = Model()

with mod:
    alpha = a

b = geweke(pymc3_obj=mod,first=0.1,last=0.1,intervals=50)
