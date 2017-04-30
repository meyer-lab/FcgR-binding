import unittest
import time
import numpy
from ..StoneModMouse import StoneModelMouse

class TestStoneModMouseFit(unittest.TestCase):

    def test_fitter(self):
    	from ..StoneModMouseFit import InVivoPredict, varyExpr

    	InVivoPredict()



if __name__ == '__main__':
    unittest.main()
