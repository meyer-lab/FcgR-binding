import unittest
import StoneModel
import numpy as np
import random
from math import *

class TestStoneMethods(unittest.TestCase):
    def setUp(self):
        self.M = StoneModel.StoneModel()

    def test_nchoosek(self):
        self.assertTrue(self.M.nchoosek(5,3) == 10)
        self.assertTrue(self.M.nchoosek(6,3) == 20)
        self.assertTrue(self.M.nchoosek(7,3) == 35)
        self.assertTrue(self.M.nchoosek(8,3) == 56)
        self.assertTrue(self.M.nchoosek(9,3) == 84)

    def test_reqFuncSolver(self):
        for xx in range(100):
            kai = random.random()
            kx = random.random()
            vi = random.randint(1, 30)
            R = random.random()
            Li = random.random()

            diffFunAnon = lambda x: R-(10**x)*(1+vi*Li*kai*(1+kx*(10**x))**(vi-1))

            output = self.M.ReqFuncSolver(R, kai, Li, vi, kx)

            self.assertTrue(abs(diffFunAnon(output)) < 1E-8)

        self.assertTrue(isnan(self.M.ReqFuncSolver(R, kai, Li, -10, kx)))

    def test_StoneMod(self):
        # This test should check that the model output satisfies Rbound = Rtot - Req
        kai = random.random()
        kx = random.random()
        v = random.randint(1, 30)
        R = random.random()
        Li = random.random()

        StoneRet = self.M.StoneMod(log10(R),kai,v,log10(kx),Li,fullOutput = True)
        Req = 10**self.M.ReqFuncSolver(R,kai,Li,v,kx)

        self.assertAlmostEqual(R, Req + StoneRet[1], delta = R/1000)

    def test_dataImport_kaBruhns(self):
        self.assertTrue(self.M.kaBruhns.shape == (6,4))

    def test_dataImport_tnpbsa(self):
        self.assertTrue(self.M.tnpbsa.shape == (2,))

    def test_dataImport_Rquant(self):
        self.assertTrue(self.M.Rquant.shape == (6,))

    def test_dataImport_mfiAdjMean1(self):
        self.assertTrue(self.M.mfiAdjMean1.shape == (24, 8))

    def test_dataImport_mfiAdjMean2(self):
        self.assertTrue(self.M.mfiAdjMean2.shape == (24, 8))

if __name__ == '__main__':
    unittest.main()
