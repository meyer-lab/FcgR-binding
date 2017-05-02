import unittest
import matplotlib.pyplot as plt
from ..StoneModel import StoneModel


class TestFigures(unittest.TestCase):
    def test_Figure4(self):
        from ..figures import Figure4

        ax = plt.gca()

        Figure4.AIplot(ax)

        Figure4.InVivoPredictVsActualAffinities(ax)

        Figure4.InVivoPredictVsActual(ax)


if __name__ == '__main__':
    unittest.main()
