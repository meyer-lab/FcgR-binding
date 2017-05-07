import unittest
import numpy
from ..StoneModel import StoneModel

class TestStoneMethods(unittest.TestCase):
    def setUp(self):
        self.M = StoneModel()
        self.Mold = StoneModel(False)

    def test_getMedianKx(self):
    	from ..StoneHelper import getMedianKx

    	outt = getMedianKx()

    	self.assertIsInstance(outt, numpy.float64)

    def test_rep(self):
    	from ..StoneHelper import rep

    	outt = rep([2, 3], 3)

    	self.assertEquals(len(outt), 6)
    	self.assertEquals(numpy.sum(outt), 15)

    	outt = rep([2, 3, 4], 4)

    	self.assertEquals(len(outt), 12)
    	self.assertEquals(numpy.sum(outt), 36)

    def test_geweke(self):
    	from ..StoneHelper import geweke

    	input = numpy.random.normal(size=4000)
    	inputTwo = numpy.random.normal(size=4000)

    	a, b = geweke(input)

    	self.assertGreater(b, 0.01)

    	a, b = geweke(input, inputTwo)

    	self.assertGreater(b, 0.01)

    	a, b = geweke(input, inputTwo + 2)

    	self.assertLess(b, 0.01)


if __name__ == '__main__':
    unittest.main()
