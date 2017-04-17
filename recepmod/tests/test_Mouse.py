import unittest
import random
import time
import pandas
import numpy as np
from ..StoneModMouse import StoneModelMouse, MultiAvidityTable, MultiAvidityPredict

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
        self.assertTrue(self.Mod.kaMouse.shape == (4,4))

    def test_dataOutput_StoneModMouse(self):
        # Checks size of fullOutput

        x = [self.logR, self.logR, self.logR, self.logR, self.logR, self.logR,
             'IgG1', self.kx, self.v, self.Li]

        out = np.array(self.Mod.StoneModMouse(x))

        self.assertTrue(out.shape == (5,4))

    def test_dataOutput_StoneModMouse2(self):
        # Checks that the model output satisfies R = Rbnd + Req

        x = [self.logR, self.logR, self.logR, self.logR, self.logR, self.logR,
             'IgG2b', self.kx, self.v, self.Li]

        a = self.Mod.StoneModMouse(x)
        b = np.array(a[1] + a[4])
        for j in range(4):
            if not np.isnan(b[j]):
                self.assertAlmostEqual(10**self.logR, b[j], delta = (10**self.logR)/10000)

    def test_pdOutputTable(self):
        # Checks the shape of pandas table from pdOutputTable

        tbfull = self.Mod.pdOutputTable(self.z)

        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(tbfull, pandas.core.frame.DataFrame)

        self.assertTrue(tbfull.shape == (4,5*len(self.Mod.FcgRs)))

    def test_pdAvidityTable(self):
        # Check shape of pandas table from pdAvidityTable
        y2 = [self.logR, self.logR, self.logR, self.logR, self.logR, self.logR,
              'IgG2a', self.kx, self.Li]

        tba2 = self.Mod.pdAvidityTable(y2, self.v, self.v+2)

        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(tba2, pandas.core.frame.DataFrame)

        self.assertTrue(tba2.shape == (3,5*len(self.Mod.FcgRs)))
        
    def test_MultiAvidityTable(self):
        # Check shape of pandas table from MultiAvidityTable
        tbM = MultiAvidityTable(self.Mod, self.z)

        MultiAvidityPredict(self.Mod, self.z, np.full((17,), 1.0, dtype=np.float64))

        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(tbM, pandas.core.frame.DataFrame)

        self.assertTrue(tbM.shape == (40,4*len(self.Mod.FcgRs)))

    def test_NimmerjahnEffectTable(self):
        tbN = self.Mod.NimmerjahnEffectTable(self.z)

        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(tbN, pandas.core.frame.DataFrame)

        self.assertTrue(tbN.shape == (8,5*len(self.Mod.FcgRs)+1))

    #def test_FcgRPlots(self):
        # Plots effectiveness vs. each FcgR binding parameter

        # self.Mod.FcgRPlots(self.z)

    def test_NimmerjahnTb_Knockdown(self):
        tbNK = self.Mod.NimmerjahnTb_Knockdown(self.z)
        # tbNK.to_csv('out.csv')
        self.Mod.NimmerjahnKnockdownLasso(self.z)
        self.Mod.KnockdownLassoCrossVal(self.z)
        self.Mod.KnockdownLassoCrossVal(self.z, logspace=True)
        self.Mod.KnockdownLassoCrossVal(self.z, addavidity1=True, printt=True)
        self.Mod.KnockdownLassoCrossVal(self.z, logspace=True, addavidity1=True)
        self.Mod.KnockdownPCA(self.z)

        self.assertTrue(tbNK.shape == (22, 17))

    def test_NimmerjahnEffectTableAffinities(self):
        """ Test that table for prediction off of just affinities is correct. """

        tbN = self.Mod.NimmerjahnEffectTableAffinities()
        # tbN.to_csv('out.csv')

        self.Mod.NimmerjahnPredictByAffinities(simple=True)
        self.Mod.NimmerjahnPredictByAffinities(fixed=True)
        self.Mod.NimmerjahnPredictByAffinities()
        self.Mod.NimmerjahnPredictByAffinities(simple=True, logspace=True)
        self.Mod.NimmerjahnPredictByAffinities(fixed=True, logspace=True)
        self.Mod.NimmerjahnPredictByAffinities(logspace=True)

        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(tbN, pandas.core.frame.DataFrame)

        self.assertTrue(tbN.shape == (11, 5))

if __name__ == '__main__':
    unittest.main()
