import unittest
from ..figures import Figure1
import numpy as np
import random
import time
from scipy.stats import norm

class TestFigMethods(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t*1000))

    def test_reqFuncSolver(self):
        variable = 2+1


if __name__ == '__main__':
    unittest.main()
