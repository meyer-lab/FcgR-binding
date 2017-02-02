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
        kx = random.random()
        v = random.randint(1, 30)
        Li = random.random()
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        x = [logR, logR, logR, logR, logR, logR, 'IgG1', kx, v, Li]
        out = np.array(self.Mod.StoneModMouse(x, fullOutput = True))
        self.assertTrue(out.shape == (5,6))
        
    def test_dataOutput_StoneModMouse2(self):
        # Checks that the model output satisfies R = Rbnd + Req
        logR = np.log10(30000*random.random())
        kx = np.array([random.random()])
        v = random.randint(1, 30)
        Li = 10**(-8)*random.random()
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        x = [logR, logR, logR, logR, logR, logR, 'IgG2b', kx, v, Li]
        a = self.Mod.StoneModMouse(x)
        b = a[1] + a[2]
        b = np.array(b)
        for j in range(5):
            if not np.isnan(b[j]):
                self.assertAlmostEqual(10**logR, b[j], delta = (10**logR)/10000)
                
    def test_pdOutputTable(self):
        # Checks the shape of pandas table from pdOutputTable
        logR = np.log10(30000*random.random())
        kx = np.array([random.random()])
        v = random.randint(1, 30)
        Li = 10**(-8)*random.random()
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        x = [logR, logR, logR, logR, logR, logR, 'IgG1', kx, v, Li]
        tb = self.Mod.pdOutputTable(x, fullOutput = False)
        self.assertTrue(tb.shape == (4,18))
        tbfull = self.Mod.pdOutputTable(x, fullOutput = True)
        self.assertTrue(tbfull.shape == (4,30))
    
    def test_pdAvidityTable(self):
        # Check shape of pandas table from pdAvidityTable
        logR = np.log10(30000*random.random())
        kx = np.array([random.random()])
        v = random.randint(1, 30)
        Li = 10**(-8)*random.random()
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        x = [logR, logR, logR, logR, logR, logR, 'IgG3', kx, v, Li]
        tba = self.Mod.pdAvidityTable(x, 4, 7, fullOutput = False)
        self.assertTrue(tba.shape == (4,18))
        x2 = [logR, logR, logR, logR, logR, logR, 'IgG2a', kx, v, Li]
        tba2 = self.Mod.pdAvidityTable(x2, v, v+2, fullOutput = False)
        self.assertTrue(tba2.shape == (3,18))
        
if __name__ == '__main__':
    unittest.main()
