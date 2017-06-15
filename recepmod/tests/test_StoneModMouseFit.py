import unittest
import pandas
from ..StoneModMouseFit import InVivoPredictMinusComponents, NimmerjahnPredictByAIratio
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")


class TestFit(unittest.TestCase):
    def test_NimmerjahnPredictByAffinities(self):
        from sklearn.metrics import r2_score
        from ..StoneModMouseFit import NimmerjahnPredictByAffinities
        output = NimmerjahnPredictByAffinities()

        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(output[2], pandas.core.frame.DataFrame)

        # Assert the explained variance we get back makes sense
        self.assertAlmostEqual(output[0],
                               r2_score(output[2].Effectiveness, output[2].DirectPredict),
                               delta=1.0E-6)
        self.assertAlmostEqual(output[1],
                               r2_score(output[2].Effectiveness, output[2].CrossPredict),
                               delta=1.0E-6)

    def test_InVivoPredictMinusComponents(self):
        InVivoPredictMinusComponents()

    def test_NimmerjahnPredictByAIratio(self):
        NimmerjahnPredictByAIratio()