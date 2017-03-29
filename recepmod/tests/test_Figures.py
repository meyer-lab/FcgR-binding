import unittest
import os
import time
import pandas
from ..figures import Figure1, Figure2
from ..StoneModel import StoneModel
from ..StoneHelper import getFitMeasMergedSummarized, read_chain, getMeasuredDataFrame

# TODO: Check the return vlues from the plotting functions

class TestFigMethods(unittest.TestCase):
    def setUp(self):
        self.M = StoneModel()
        self.startTime = time.time()
        self.Mread, self.dset = read_chain(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/test_chain.h5"))

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t*1000))

    def test_kaBinding_plot(self):
        # Return the fit and binding data summary data set
        fitMean = getFitMeasMergedSummarized(self.M, self.M.lb)

        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(fitMean, pandas.core.frame.DataFrame)

        # Create the measured binding vs. ka plot
        Figure1.plotNormalizedBindingvsKA(fitMean)

        # Create avidity effect vs. Ka plot
        Figure1.plotAvidityEffectVsKA(fitMean)

    # Test mfiAdjMean plot
    def test_mfiAdjMean_figure(self):
        # Call the plotting function
        Figure1.mfiAdjMeanFigureMaker(getMeasuredDataFrame(self.M))

    # Test the predicted vs. measured plot
    def test_Fig2_plots(self):
        # Create the data and fit frame based on the lower bounds values
        fitFrame = getFitMeasMergedSummarized(self.M, self.M.lb)

        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(fitFrame, pandas.core.frame.DataFrame)

        # Create fit of measured vs. predicted
        Figure2.plotFit(fitFrame)

        # Create the LL of the fit plot
        Figure2.plotQuant(fitFrame, 'Meas_mean', 'Meas_mean')

    # Test hist subplots
    def test_Fig2_histSubplots(self):

        Figure2.histSubplots(self.dset)

if __name__ == '__main__':
    unittest.main()
