import unittest
import time
import numpy
from ..StoneModel import StoneModel

class TestStoneMethods(unittest.TestCase):
    def setUp(self):
        self.M = StoneModel()
        self.Mold = StoneModel(False)
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t*1000))

    def test_getMedianKx(self):
    	from ..StoneHelper import getMedianKx

    	outt = getMedianKx()

    	self.assertIsInstance(outt, numpy.float64)


if __name__ == '__main__':
    unittest.main()
