import unittest
import random
import time
import numpy as np
from ..StoneModMouse import StoneModelMouse

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
        logR = np.log10(24000)
        kx = 10**(-7)
        v = 5
        Li = 10**(-9)
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        x = [logR, logR, logR, logR, logR, logR, 'IgG1', kx, v, Li]
        out = np.array(self.Mod.StoneModMouse(x))
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
        b = np.array(a[1] + a[4])
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
        tbfull = self.Mod.pdOutputTable(z)
        self.assertTrue(tbfull.shape == (4,30))

    def test_pdAvidityTable(self):
        # Check shape of pandas table from pdAvidityTable
        logR = np.log10(30000*random.random())
        kx = random.random()
        v = random.randint(1, 30)
        Li = 10**(-8)*random.random()
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        y2 = [logR, logR, logR, logR, logR, logR, 'IgG2a', kx, Li]
        tba2 = self.Mod.pdAvidityTable(y2, v, v+2)
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
        res = self.Mod.NimmerjahnLasso(zN)
        res2 = self.Mod.NimmerjahnLassoCrossVal(zN)

        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(res, np.ndarray)

    def test_FcgRPlots(self):
        # Plots effectiveness vs. each FcgR binding parameter
        logR = np.log10(10**5)
        kx = 10**(-7)
        v = 10
        Li = 10**(-9)
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        zN = [logR, logR, logR, logR, logR, logR, kx, v, Li]
        self.Mod.FcgRPlots(zN)

    def test_RmultiAvidityTable(self):
        # Plots effectiveness vs. each FcgR binding parameter
        logR = np.log10(10**5)
        kx = 10**(-7)
        v = 5
        Li = 7*10**(-9)
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        x = [logR, logR, logR, logR, logR, logR, 'IgG1', kx, v, Li]
        z = [logR, logR, logR, logR, logR, logR, kx, v, Li]
        Rmultiv = self.Mod.RmultiAvidity(x)
        self.Mod.RmultiAvidityTable(z)
        self.assertTrue(Rmultiv.shape == (6,v))

    def test_NimmerjahnTb_Knockdown(self):
        logR = np.log10(10**5)
        kx = 10**(-7)
        v = 10
        Li = 10**(-9)
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        z = [logR, logR, logR, logR, logR, logR, kx, v, Li]
        tbNK = self.Mod.NimmerjahnTb_Knockdown(z)
        tbNK.to_csv('out.csv')
        self.Mod.NimmerjahnKnockdownLasso(z)
        self.Mod.KnockdownLassoCrossVal(z)
        #self.Mod.KnockdownLassoCrossVal(z, logspace = True)
        self.Mod.KnockdownLassoCrossVal2(z)
        self.Mod.KnockdownLassoCrossVal3(z)
        self.Mod.KnockdownPCA(z)
        self.assertTrue(tbNK.shape == (18,25))

    def test_Knockdown_Tree(self):
        logR = np.log10(10**5)
        kx = 10**(-7)
        v = 10
        Li = 10**(-9)
        if logR < 0 or kx < 0 or v < 0 or Li < 0:
            raise ValueError('Negative input parameters')
        z = [logR, logR, logR, logR, logR, logR, kx, v, Li]
        self.Mod.DecisionTree(z)
        self.Mod.DecisionTree2(z)
        self.Mod.DecisionTree3(z)
        self.Mod.DecisionTree(z, logspace = True)
        self.Mod.DecisionTree2(z, logspace = True)
        output = self.Mod.DecisionTree3(z, logspace = True)
        self.assertTrue(len(output) == 9)

if __name__ == '__main__':
    unittest.main()
