import unittest
import random
import time
import pandas
import numpy as np
from ..StoneModMouse import StoneModelMouse, MultiAvidityPredict

class TestStoneMouse(unittest.TestCase):
    def setUp(self):
        self.Mod = StoneModelMouse()

    def test_dataImport_kaMouse(self):
        self.assertTrue(self.Mod.kaMouse.shape == (4, 4))
        self.assertTrue(self.Mod.kaIgG2b_Fucose.shape == (4,1))

    def test_dataOutput_StoneModMouse(self):
        # Checks size of fullOutput
        out = np.array(self.Mod.StoneModMouse())

        self.assertTrue(out.shape == (4, 5, 4))

    def test_dataOutput_StoneModMouse2(self):
        # Checks that the model output satisfies R = Rbnd + Req

        a = self.Mod.StoneModMouse()
        
        for i in range(len(self.Mod.Igs)):
            for j in range(len(self.Mod.FcgRs)):
                if not np.isnan(a[i, 1, j]):
                    self.assertAlmostEqual(10**self.Mod.logR[j], 
                                           a[i, 1, j] + a[i, 4, j], 
                                           delta = (10**self.Mod.logR[j])/10000)

    def test_pdOutputTable(self):
        """ Checks the shape of pandas table from pdOutputTable """

        tbfull = self.Mod.pdOutputTable()

        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(tbfull, pandas.core.frame.DataFrame)

        self.assertTrue(tbfull.shape == (4,5*len(self.Mod.FcgRs)))

    def test_pdAvidityTable(self):
        """ Checks pdAvidityTable """
        # Check shape of pandas table from pdAvidityTable
        tba2 = self.Mod.pdAvidityTable()
        
        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(tba2, pandas.core.frame.DataFrame)

        self.assertTrue(tba2.shape == (self.Mod.v*len(self.Mod.Igs),5*len(self.Mod.FcgRs)))
        
    def test_NimmerjahnEffectTable(self):
        """ Check NimmerjahnEffectTable """
        tbN = self.Mod.NimmerjahnEffectTable()

        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(tbN, pandas.core.frame.DataFrame)

        self.assertTrue(tbN.shape == (8,5*len(self.Mod.FcgRs)+1))

    def test_NimmerjahnEffectTableAffinities(self):
        """ Test that table for prediction off of just affinities is correct. """
        tbN = self.Mod.NimmerjahnEffectTableAffinities()

        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(tbN, pandas.core.frame.DataFrame)

        self.assertTrue(tbN.shape == (12, 5))

    def test_PCA(self):
        scores, expVar = self.Mod.PCA()
        
        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(scores, pandas.core.frame.DataFrame)

if __name__ == '__main__':
    unittest.main()