import matlab.engine as m
import matlab
from math import *
from ReqFuncSolver import diffFun
from ReqFuncSolver import ReqFuncSolver

eng = m.start_matlab()
##a = eng.temp(3000.0,1.0e-7,7.0e-8,4.0,1.0e-8)
##a = eng.temp2(3.0,3000.0,4.0,1.0e-8,4.0e-4)

##b = ReqFuncSolver(3000,1e-7,7e-8,4,1e-8)
##b = diffFun(3,3000,4,1e-8,4e-4)

print(10**(-20)-eng.temp3(10.0,-20.0))
