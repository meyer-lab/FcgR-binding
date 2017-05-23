import unittest
import matplotlib.pyplot as plt


class TestFigures(unittest.TestCase):
    def test_Figure4(self):
        from ..figures import Figure4
        from ..figures import Figure2

        ax = plt.gca()

        Figure4.AIplot(ax)

        Figure4.InVivoPredictVsActualAffinities(ax)

        Figure4.InVivoPredictVsActual(ax)

        Figure4.InVivoPredictComponents(ax)

        Figure4.ComponentContrib(ax)

        Figure4.RequiredComponents(ax)

        Figure2.AverageAvidity(ax)


if __name__ == '__main__':
    unittest.main()
