import unittest
import time
import pandas
from ..ValidationOrtiz import Ortiz

class TestOrtizMethods(unittest.TestCase):
    def setUp(self):
        self.Ortiz = Ortiz()

    def test_classSetup(self):
        # Make sure we were given a Pandas dataframe
        self.assertIsInstance(self.Ortiz.FcResponse, pandas.core.frame.DataFrame)

    def test_predictResponse(self):
        # Run prediction
        self.Ortiz.predictResponse()

if __name__ == '__main__':
    unittest.main()
