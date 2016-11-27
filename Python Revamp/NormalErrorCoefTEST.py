import matlab.engine
import numpy as np
from NormalErrorCoef import NormalErrorCoef
from loadData import loadData

eng = matlab.engine.start_matlab()
a = np.array([[1,0],[0,1]])
test = eng.eye(5)
print(type(test))
