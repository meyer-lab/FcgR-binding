import unittest
import StoneModel
import numpy as np
import random
import time
from scipy.stats import norm

class TestStoneMethods(unittest.TestCase):
    def setUp(self):
        self.M = StoneModel.StoneModel()
        self.Mold = StoneModel.StoneModel(False)
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t*1000))

    def test_nchoosek(self):
        self.assertTrue(StoneModel.nchoosek(5,3) == 10)
        self.assertTrue(StoneModel.nchoosek(6,3) == 20)
        self.assertTrue(StoneModel.nchoosek(7,3) == 35)
        self.assertTrue(StoneModel.nchoosek(8,3) == 56)
        self.assertTrue(StoneModel.nchoosek(9,3) == 84)

    def test_reqFuncSolver(self):
        for xx in range(100):
            kai = random.random()
            kx = random.random()
            vi = random.randint(1, 30)
            R = random.random()
            Li = random.random()

            diffFunAnon = lambda x: R-(10**x)*(1+vi*Li*kai*(1+kx*(10**x))**(vi-1))

            output = StoneModel.ReqFuncSolver(R, kai, Li, vi, kx)

            self.assertTrue(abs(diffFunAnon(output)) < 1E-8)

        self.assertTrue(np.isnan(StoneModel.ReqFuncSolver(R, kai, Li, -10, kx)))

    def test_StoneMod(self):
        # This test should check that the model output satisfies Rbound = Rtot - Req
        kai = random.random()
        kx = random.random()
        v = random.randint(1, 30)
        R = random.random()
        Li = random.random()

        StoneRet = self.M.StoneMod(np.log10(R),kai,v,np.log10(kx),Li,fullOutput = True)
        Req = 10**StoneModel.ReqFuncSolver(R,kai,Li,v,kx)

        self.assertAlmostEqual(R, Req + StoneRet[1], delta = R/1000)

    def test_dataImport_kaBruhns(self):
        self.assertTrue(self.M.kaBruhns.shape == (6,4))

    def test_dataImport_tnpbsa(self):
        self.assertTrue(self.M.tnpbsa.shape == (2,))

    def test_dataImport_Rquant(self):
        self.assertTrue(self.M.Rquant.shape == (6,))

    def test_dataImport_mfiAdjMean(self):
        self.assertTrue(self.M.mfiAdjMean.shape == (24, 8))
        self.assertTrue(self.Mold.mfiAdjMean.shape == (24, 8))

    def test_NormalErrorCoef(self):
        retVal = self.M.NormalErrorCoef(self.M.lb)

        self.assertFalse(np.isnan(retVal))
        self.assertFalse(np.isinf(retVal))

    def test_logpdf(self):
        vecIn = np.array([0.01, 0.2, 0.3, 0.4])

        self.assertAlmostEqual(norm.logpdf(vecIn, 0.2, 1).sum(), StoneModel.logpdf_sum(vecIn, 0.2, 1), 0.000001)


if __name__ == '__main__':
    unittest.main()
