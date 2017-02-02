import unittest
from ..figures import Figure1
from ..figures import Figure2
from ..figures import Figure3
from ..figures import Figure4
from ..figures import Figure5
import numpy as np
import random
import time
from ..StoneModel import StoneModel
from ..StoneHelper import getFitMeasMergedSummarized

class TestFigMethods(unittest.TestCase):
    def setUp(self):
        self.M = StoneModel()
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t*1000))

    def test_kaBinding_plot(self):
        # Return the fit and binding data summary data set
        fitMean = getFitMeasMergedSummarized(self.M, self.M.lb)

        # Create the measured binding vs. ka plot
        Figure1.plotNormalizedBindingvsKA(fitMean)

        self.assertTrue(True)

    # Test mfiAdjMean plot
    def test_mfiAdjMean_figure(self):
        # Call the plotting function
        Figure1.mfiAdjMeanFigureMaker(self.M)

        self.assertTrue(True)

    # Test the predicted vs. measured plot
    def test_plotFit_plot(self):
        # Create the data and fit frame based on the lower bounds values
        fitFrame = getFitMeasMergedSummarized(self.M, self.M.lb)

        # Create fit of measured vs. predicted
        Figure2.plotFit(fitFrame)

        self.assertTrue(True)

    # Test LL plot
    def test_plotQuant_plot(self):
        # Create the data and fit frame based on the lower bounds values
        fitFrame = getFitMeasMergedSummarized(self.M, self.M.lb)

        # Create the LL of the fit plot
        Figure2.plotQuant(fitFrame, 'Meas_mean', 'Meas_mean')

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
