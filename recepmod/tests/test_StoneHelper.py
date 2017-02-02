import unittest
import random
import time
from ..StoneHelper import *
from ..StoneModel import StoneModel

class TestStoneMethods(unittest.TestCase):
    def setUp(self):
        self.M = StoneModel()
        self.Mold = StoneModel(False)
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t*1000))

    # From here down test that the various plotting functions correctly run
    # TODO: Add these plots for the old model

    # Test the predicted vs. measured plot
    def test_plotFit_plot(self):
        # Create the data and fit frame based on the lower bounds values
        fitFrame = getFitMeasMergedSummarized(self.M, self.M.lb)

        # Create fit of measured vs. predicted
        plotFit(fitFrame)

        self.assertTrue(True)

    # Test LL plot
    def test_plotQuant_plot(self):
        # Create the data and fit frame based on the lower bounds values
        fitFrame = getFitMeasMergedSummarized(self.M, self.M.lb)

        # Create the LL of the fit plot
        plotQuant(fitFrame, 'Meas_mean', 'Meas_mean')

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
