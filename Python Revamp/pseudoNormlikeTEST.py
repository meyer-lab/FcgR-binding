import pseudoNormlike as ps
import matlab.engine
import numpy as np

## This code is written to determine whether the Python script pseudoNormlike,
## based off the MATLAB function normlike, is written properly. The code below
## shows differences in log likelihoods of the order of magnitude of 1e-16, on
## the occasion that such discrepency exists. Therefore, I consider pseudoNormlike
## to behave properly.

## Initiate MATLAB engine
eng = matlab.engine.start_matlab()

## Compare values of pseudoNormlike to values of MATLAB's normlike
for j in range(100):
    print(j)
    temp = np.random.rand(3)
    temp0 = float(temp[0])
    temp1 = float(temp[1])
    temp2 = float(temp[2])
    test = ps.pseudoNormlike(temp0,temp1,temp2)-eng.normlikeTEMP(temp0, \
                                                                temp1, \
                                                                temp2)
    if test != 0.0:
        print(False)
        print(test)
        print('\n')
