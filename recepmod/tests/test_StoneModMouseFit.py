import unittest
import time
import numpy
from ..StoneModMouse import StoneModelMouse

class TestStoneModMouseFit(unittest.TestCase):
    def setUp(self):
        self.M = StoneModelMouse()

    def test_fitter(self):
    	from ..StoneModMouseFit import InVivoPredict

    	InVivoPredict(self.M)



if __name__ == '__main__':
    unittest.main()
