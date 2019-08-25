import unittest
import numpy
from ..StoneModel import StoneModel

# pylint: disable=R0201


class TestStoneMethods(unittest.TestCase):
    def setUp(self):
        self.M = StoneModel()
        self.Mold = StoneModel(False)

    def test_getMedianKx(self):
        """ Test that median Kx returns a float. """
        from ..StoneHelper import getMedianKx

        outt = getMedianKx()

        self.assertIsInstance(outt, numpy.float64)

    def test_rep(self):
        """ Test the rep method. """
        from ..StoneHelper import rep

        outt = rep([2, 3], 3)

        self.assertEqual(len(outt), 6)
        self.assertEqual(numpy.sum(outt), 15)

        outt = rep([2, 3, 4], 4)

        self.assertEqual(len(outt), 12)
        self.assertEqual(numpy.sum(outt), 36)

    def test_geweke(self):
        """ Test the geweke method. """
        from ..StoneHelper import geweke

        numpy.random.seed(0)

        inputt = numpy.random.normal(size=4000)
        inputTwo = numpy.random.normal(size=4000)

        _, b = geweke(inputt)

        self.assertGreater(b, 0.01)

        _, b = geweke(inputt, inputTwo)

        self.assertGreater(b, 0.01)

        _, b = geweke(inputt, inputTwo + 2)

        self.assertLess(b, 0.01)

    def test_geweke_chain(self):
        """ Test the geweke chain method. """
        from ..StoneHelper import geweke_chain
        import pandas as pd

        numpy.random.seed(0)

        data = pd.DataFrame(numpy.random.normal(size=(4000, 10)))
        data['LL'] = 1
        data['walker'] = 1

        _, b = geweke_chain(data)

        self.assertGreater(numpy.min(b), 0.01)
        self.assertEqual(len(b), 10)


if __name__ == '__main__':
    unittest.main()
