from ReqFuncSolver import *
import time
from loadData import loadData
import numpy as np

data = loadData()

kai = 3*np.random.rand(100)+5
R = 2*np.random.rand(100)+3
logkx = 8*np.random.rand(100)-12
kx = 10**logkx
Li = 7e8
vi = np.random.randint(1,30,100)

start = time.time()
for j in range(100):
    Req = ReqFuncSolver(R[j], kai[j], Li, vi[j], kx[j])
end = time.time()

print(end-start)
