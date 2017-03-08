import unittest
from ..StoneModMouse import StoneModelMouse
import numpy as np
import random
import time
from scipy.stats import norm
import matplotlib

class TestStoneMouse(unittest.TestCase):
    def setUp(self):
        self.Mod = StoneModelMouse()
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
        kx = random.random()
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
        kx = random.random()
        v = random.randint(1, 30)
        Li = 10**(-8)*random.random()
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        z = [logR, logR, logR, logR, logR, logR, kx, v, Li]
        tb = self.Mod.pdOutputTable(z, fullOutput = False)
        self.assertTrue(tb.shape == (4,18))
        tbfull = self.Mod.pdOutputTable(z, fullOutput = True)
        self.assertTrue(tbfull.shape == (4,30))

    def test_pdAvidityTable(self):
        # Check shape of pandas table from pdAvidityTable
        logR = np.log10(30000*random.random())
        kx = random.random()
        v = random.randint(1, 30)
        Li = 10**(-8)*random.random()
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        y = [logR, logR, logR, logR, logR, logR, 'IgG3', kx, Li]
        tba = self.Mod.pdAvidityTable(y, 4, 7, fullOutput = False)
        self.assertTrue(tba.shape == (4,18))
        y2 = [logR, logR, logR, logR, logR, logR, 'IgG2a', kx, Li]
        tba2 = self.Mod.pdAvidityTable(y2, v, v+2, fullOutput = True)
        self.assertTrue(tba2.shape == (3,30))

    def test_NimmerjahnEffectTable(self):
        logR = np.log10(10**5)
        kx = 10**(-7)
        v = 10
        Li = 10**(-9)
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        z = [logR, logR, logR, logR, logR, logR, kx, v, Li]
        tbN = self.Mod.NimmerjahnEffectTable(z)
        #print(tbN.iloc[:, list(range(10,20))])
        self.assertTrue(tbN.shape == (8,31))
		
    def test_NimmerjahnMultiLinear(self):
        # Prints coefficients of multi-linear regression model
        logR = np.log10(10**5)
        kx = 10**(-7)
        v = 10
        Li = 10**(-9)
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        zN = [logR, logR, logR, logR, logR, logR, kx, v, Li]
        result = self.Mod.NimmerjahnMultiLinear(zN)
        #print(result.coef_)
        res = self.Mod.NimmerjahnLasso(zN)
        #print(res.coef_)
    
    def test_FcgRPlots(self):
        # Plots effectiveness vs. each FcgR binding parameter
        logR = np.log10(10**5)
        kx = 10**(-7)
        v = 10
        Li = 10**(-9)
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        zN = [logR, logR, logR, logR, logR, logR, kx, v, Li]
        plots = self.Mod.FcgRPlots(zN)

    def test_RmultiAvidityTable(self):
        # Plots effectiveness vs. each FcgR binding parameter
        logR = np.log10(10**5)
        kx = 10**(-7)
        v = 5
        Li = 10**(-9)
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        x = [logR, logR, logR, logR, logR, logR, 'IgG1', kx, v, Li]
        z = [logR, logR, logR, logR, logR, logR, kx, v, Li]
        Rmultiv = self.Mod.RmultiAvidity(x)
        RmultivTb = self.Mod.RmultiAvidityTable(z)
        #print(RmultivTb)
        self.assertTrue(Rmultiv.shape == (6,v))

if __name__ == '__main__':
    unittest.main()