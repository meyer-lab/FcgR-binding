import unittest
import random
import time
import numpy as np
from ..StoneModMouse import StoneModelMouse

class TestStoneMouse(unittest.TestCase):
    def setUp(self):
        self.Mod = StoneModelMouse()
        self.startTime = time.time()
        self.kx = 10**(-12.25)
        self.logR = np.log10(10**5)
        self.v = 10
        self.Li = 10**(-9)
        self.z = [self.logR, self.logR, self.logR, self.logR, self.logR,
                  self.logR, self.kx, self.v, self.Li]

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t*1000))

    def test_dataImport_kaMouse(self):
        self.assertTrue(self.Mod.kaMouse.shape == (6,4))

    def test_dataOutput_StoneModMouse(self):
        # Checks size of fullOutput

        x = [self.logR, self.logR, self.logR, self.logR, self.logR, self.logR,
             'IgG1', self.kx, self.v, self.Li]

        out = np.array(self.Mod.StoneModMouse(x))
        self.assertTrue(out.shape == (5,6))

    def test_dataOutput_StoneModMouse2(self):
        # Checks that the model output satisfies R = Rbnd + Req

        x = [self.logR, self.logR, self.logR, self.logR, self.logR, self.logR,
             'IgG2b', self.kx, self.v, self.Li]

        a = self.Mod.StoneModMouse(x)
        b = np.array(a[1] + a[4])
        for j in range(5):
            if not np.isnan(b[j]):
                self.assertAlmostEqual(10**self.logR, b[j], delta = (10**self.logR)/10000)

    def test_pdOutputTable(self):
        # Checks the shape of pandas table from pdOutputTable

        tbfull = self.Mod.pdOutputTable(self.z)
        self.assertTrue(tbfull.shape == (4,30))

    def test_pdAvidityTable(self):
        # Check shape of pandas table from pdAvidityTable
        logR = np.log10(30000*random.random())

        if logR < 0:
            raise ValueError('Negative input parameters')
        y2 = [logR, logR, logR, logR, logR, logR, 'IgG2a', self.kx, self.Li]
        tba2 = self.Mod.pdAvidityTable(y2, self.v, self.v+2)
        self.assertTrue(tba2.shape == (3,30))

    def test_NimmerjahnEffectTable(self):
        tbN = self.Mod.NimmerjahnEffectTable(self.z)

        self.assertTrue(tbN.shape == (8,31))

    def test_NimmerjahnMultiLinear(self):
        # Prints coefficients of multi-linear regression model

        self.Mod.NimmerjahnMultiLinear(self.z)
        res = self.Mod.NimmerjahnLasso(self.z)
        self.Mod.NimmerjahnLassoCrossVal(self.z)

        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(res, np.ndarray)

    def test_FcgRPlots(self):
        # Plots effectiveness vs. each FcgR binding parameter

        self.Mod.FcgRPlots(self.z)

    def test_NimmerjahnTb_Knockdown(self):
        tbNK = self.Mod.NimmerjahnTb_Knockdown(self.z)
        # tbNK.to_csv('out.csv')
        self.Mod.NimmerjahnKnockdownLasso(self.z)
        self.Mod.KnockdownLassoCrossVal(self.z)
        #self.Mod.KnockdownLassoCrossVal(self.z, logspace = True)
        self.Mod.KnockdownLassoCrossVal2(self.z)
        self.Mod.KnockdownLassoCrossVal3(self.z)
        self.Mod.KnockdownPCA(self.z)
        self.assertTrue(tbNK.shape == (18, 25))

if __name__ == '__main__':
    unittest.main()
