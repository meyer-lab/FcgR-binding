import unittest
from ..StoneModel import *
import numpy as np
import random
import time
from scipy.stats import norm

class TestStoneMethods(unittest.TestCase):
    def setUp(self):
        self.M = StoneModel()
        self.Mold = StoneModel(False)
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t*1000))

    def test_nchoosek(self):
        self.assertTrue(nchoosek(5,3) == 10)
        self.assertTrue(nchoosek(6,3) == 20)
        self.assertTrue(nchoosek(7,3) == 35)
        self.assertTrue(nchoosek(8,3) == 56)
        self.assertTrue(nchoosek(9,3) == 84)

    def test_reqFuncSolver(self):
        for xx in range(100):
            kai = random.random()
            kx = random.random()
            vi = random.randint(1, 30)
            R = random.random()
            Li = random.random()

            diffFunAnon = lambda x: R-(10**x)*(1+vi*Li*kai*(1+kx*(10**x))**(vi-1))

            output = ReqFuncSolver(R, kai, Li, vi, kx)

            self.assertTrue(abs(diffFunAnon(output)) < 1E-8)

        self.assertTrue(np.isnan(ReqFuncSolver(R, kai, Li, -10, kx)))

    def test_StoneMod(self):
        # This test should check that the model output satisfies Rbound = Rtot - Req
        kai = random.random()
        kx = random.random()
        v = random.randint(1, 30)
        R = random.random()
        Li = random.random()

        StoneRet = StoneMod(np.log10(R),kai,v,kx,Li,fullOutput = True)
        Req = 10**ReqFuncSolver(R,kai,Li,v,kx)

        self.assertAlmostEqual(R, Req + StoneRet[1], delta = R/1000)

    # Test that monovalent ligand follows the binding curve
    def test_StoneModTwo(self):
        # logR,Ka,v,logKx,L0

        # Sweep across ligand concentration
        for i in range(100):
            L = i / 100.0

            StoneRet = StoneMod(0.0,1,1,3,L)

            self.assertAlmostEqual(StoneRet[0], L / (1 + L), delta = 0.0001)

    def test_dataImport_kaBruhns(self):
        self.assertTrue(self.M.kaBruhns.shape == (6,4))

    def test_dataImport_tnpbsa(self):
        self.assertTrue(self.M.tnpbsa.shape == (2,))

    def test_dataImport_Rquant(self):
        self.assertTrue(len(self.M.Rquant) == 6)

    def test_Stone_names(self):
        self.assertEqual(len(self.M.pNames), self.M.lb.shape[0])
        self.assertEqual(len(self.Mold.pNames), self.Mold.lb.shape[0])

    def test_dataImport_mfiAdjMean(self):
        self.assertTrue(self.M.mfiAdjMean.shape == (24, 8))
        self.assertTrue(self.Mold.mfiAdjMean.shape == (24, 8))

    def test_NormalErrorCoef(self):
        retVal = self.M.NormalErrorCoef(self.M.lb)

        self.assertFalse(np.isnan(retVal))
        self.assertFalse(np.isinf(retVal))

    # Test that our hand-coded logpdf matches the results of SciPy
    def test_logpdf(self):
        vecIn = np.array([0.01, 0.2, 0.3, 0.4])

        self.assertAlmostEqual(norm.logpdf(vecIn, 0.2, 1).sum(), logpdf_sum(vecIn, 0.2, 1), 0.000001)


if __name__ == '__main__':
    unittest.main()
