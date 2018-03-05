import unittest
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

# pylint: disable=R0201


class TestFigures(unittest.TestCase):
    def test_Figure4(self):
        from ..figures import Figure4

        ax = plt.gca()

        Figure4.InVivoPredictComponents(ax)

        Figure4.ComponentContrib(ax)

        Figure4.AffinityPredict(ax)

    def test_Figure2_AvgAV(self):
        from ..figures import Figure2

        ax = plt.gca()

        Figure2.AverageAvidity(ax)

    def test_Figure4_AI(self):
        from ..figures import Figure4

        ax = plt.gca()

        Figure4.AIplot(ax)

    def test_Figure4_ReqComp(self):
        from ..figures import Figure4

        ax = plt.gca()

        Figure4.RequiredComponents(ax)

    def test_Figure4_predVact(self):
        from ..figures import Figure4

        ax = plt.gca()

        Figure4.InVivoPredictVsActual(ax)

    def test_Figure4_predAffinity(self):
        from ..figures import Figure4

        ax = plt.gca()

        Figure4.InVivoPredictVsActualAffinities(ax)


if __name__ == '__main__':
    unittest.main()
