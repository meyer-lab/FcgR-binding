import unittest
import sys

sys.path.append('../')

import StoneModMouse
import numpy as np
import random
import time
from scipy.stats import norm
import matplotlib

class TestStoneMouse(unittest.TestCase):
    def setUp(self):
        self.Mod = StoneModMouse.StoneModelMouse()
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t*1000))

    def test_dataImport_kaMouse(self):
        self.assertTrue(self.Mod.kaMouse.shape == (6,4))

    def test_dataOutput_StoneModMouse(self):
        # Checks size of fullOutput
        logR = np.log10(30000*random.random())
        kx = np.array([random.random()])
        v = random.randint(1, 30)
        Li = random.random()
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        x = [logR, logR, logR, logR, logR, logR, 'IgG3', kx, v, Li]
        out = np.array(self.Mod.StoneModMouse(x, fullOutput = True))
        self.assertTrue(out.shape == (5,6))

    def test_dataOutput_StoneModMouse2(self):
        # Checks that the model output satisfies R = Rbnd + Req
        logR = np.log10(30000*random.random())
        kx = np.array([random.random()])
        v = random.randint(1, 30)
        Li = random.random()
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        x = [logR, logR, logR, logR, logR, logR, 'IgG2b', kx, v, Li]
        a = self.Mod.StoneModMouse(x)
        b = a[1] + a[2]
        b = np.array(b)
        for i in range(5):
            if not np.isnan(b[i]):
                self.assertAlmostEqual(10**logR, b[i], delta = (10**logR)/10000)

if __name__ == '__main__':
    unittest.main()
