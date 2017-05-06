import unittest
import random
import time
import pandas
import numpy as np
from ..StoneModMouseFit import NimmerjahnPredictByAffinities, InVivoPredictMinusComponents, NimmerjahnPredictByAIratio
from sklearn.metrics import explained_variance_score

class TestFit(unittest.TestCase):
    def test_NimmerjahnPredictByAffinities(self):
        output = NimmerjahnPredictByAffinities()

        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(output[2], pandas.core.frame.DataFrame)

        # Assert the explained variance we get back makes sense
        self.assertAlmostEqual(output[0],
                               explained_variance_score(output[2].Effectiveness, output[2].DirectPredict),
                               delta = 1.0E-6)
        self.assertAlmostEqual(output[1], 
                               explained_variance_score(output[2].Effectiveness, output[2].CrossPredict),
                               delta = 1.0E-6)

    def test_InVivoPredictMinusComponents(self):
        InVivoPredictMinusComponents()
    
    def test_NimmerjahnPredictByAIratio(self):
        NimmerjahnPredictByAIratio()