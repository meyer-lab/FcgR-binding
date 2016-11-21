from loadData import loadData
import matlab.engine
import numpy as np
from math import *
from StoneMod import StoneMod

##eng = matlab.engine.start_matlab()

data = loadData()

biCoefMat = data['biCoefMat']
tnpbsa = data['tnpbsa']
L0 = tnpbsa[0]

go = True
while go:
    query = input('Continue?')
    if query == 'yes':
        R = 50000*np.random.rand(1)
        logR = log10(R)
        Ka = 10**(np.random.rand(1)+5)
        logKx = 8*np.random.rand(1)-12
        v = np.random.randint(1,30)
        
        temp = StoneMod(logR,Ka,v,logKx,L0,biCoefMat)
    elif query == 'naw':
        go = False
