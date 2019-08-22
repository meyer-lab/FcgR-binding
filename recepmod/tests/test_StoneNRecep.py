import unittest
import itertools
import numpy as np
from ..StoneNRecep import StoneVgrid, reqSolver, StoneRbnd, StoneN


class TestStoneNRecpMethods(unittest.TestCase):
    def test_StoneVgrid(self):
        Req = np.array([1000, 1000], dtype=np.float64)
        Ka = np.array([1000, 2000], dtype=np.float64)
        L0 = 1.000E-7
        Kx = 1.0E-5
        gnu = 4

        output = StoneVgrid(Req, Ka, gnu, Kx, L0)

        # Check that the grid is setup appropriately
        for ii in range(gnu + 1):
            for jj in range(gnu + 1):
                if ii + jj > gnu:
                    self.assertEqual(output[ii, jj], 0)
                elif ii == 0 and jj == 0:
                    self.assertEqual(output[ii, jj], 0)
                else:
                    self.assertNotEqual(output[ii, jj], 0)

        # Kx is specified in the reference of the first receptor
        Kx = Ka[1] / Ka[0] * Kx

        # Assemble the grid for the mirror case
        output2 = StoneVgrid(np.flipud(Req), np.flipud(Ka), gnu, Kx, L0)

        # Check that detailed balance holds
        self.assertTrue(np.all(np.isclose(output, np.transpose(output2))))

    def test_boundMult(self):
        from itertools import permutations
        from ..StoneNRecep import boundMult

        for ii in range(2, 5):
            self.assertEqual(boundMult([0] * ii), 1)

        for ii in range(1, 10):
            self.assertEqual(boundMult([ii, 0, 0, 0, 0]), 1)

        a = [10, 0, 0, 0, 0, 0]
        for perm in permutations(a):
            self.assertEqual(boundMult(perm), 1)

        a = [3, 1, 0, 0, 0, 0]
        for perm in permutations(a):
            self.assertEqual(boundMult(perm), 4, "Testing vector: " + str(perm))

        a = [3, 1, 1, 0, 0, 0]
        for perm in permutations(a):
            self.assertEqual(boundMult(perm), 20, "Testing vector: " + str(perm))

    def test_vGridVar(self):
        """ Test that varying Req and Ka provides the expected results. """
        Req = np.array([1E4, 1E3], dtype=np.float64)
        Ka = np.array([1E3, 1E3], dtype=np.float64)
        L0 = 1.000E-7
        Kx = 1.0E-5
        gnu = 4

        output = StoneVgrid(Req, Ka, gnu, Kx, L0)
        self.assertGreater(output[3, 0], output[0, 3])

        Req = np.flipud(Req)
        output = StoneVgrid(Req, Ka, gnu, Kx, L0)
        self.assertLess(output[3, 0], output[0, 3])

        Req[0:2] = [1E3, 1E3]
        Ka[0:2] = [1E4, 1E3]

        output = StoneVgrid(Req, Ka, gnu, Kx, L0)
        self.assertGreater(output[3, 0], output[0, 3])

        Ka = np.flipud(Ka)
        output = StoneVgrid(Req, Ka, gnu, Kx, L0)
        self.assertLess(output[3, 0], output[0, 3])

    def test_StoneRbnd(self):
        from ..StoneNRecep import StoneRmultiAll

        gnu = 4

        vGrid = np.ones([gnu + 1, gnu + 1], dtype=np.float64)
        vGrid[0, 0] = 0

        for ii in range(vGrid.shape[0]):
            for jj in range(vGrid.shape[0]):
                if ii + jj > gnu:
                    vGrid[ii, jj] = 0

        output = StoneRbnd(vGrid)
        outputmulti = StoneRmultiAll(vGrid)

        self.assertEqual(output[0], 20)
        self.assertEqual(output[1], 20)
        self.assertEqual(outputmulti[0], 19)
        self.assertEqual(outputmulti[1], 19)

        vGrid[2, 0] = 2

        output = StoneRbnd(vGrid)
        outputmulti = StoneRmultiAll(vGrid)

        self.assertEqual(output[0], 22)
        self.assertEqual(output[1], 20)
        self.assertEqual(outputmulti[0], 21)
        self.assertEqual(outputmulti[1], 19)

    # This processes checks that the relationships with Rbnd make sense when
    # considering variation in Req and Ka
    def test_Rbnd_vGrid(self):
        logR = np.array([3, 2], dtype=np.float64)
        Ka = np.array([1E4, 1E4], dtype=np.float64)
        gnu = 10
        Kx = 1E-5
        L0 = 1E-5

        Rbnd = StoneRbnd(StoneVgrid(np.power(10, logR), Ka, gnu, Kx, L0))

        self.assertGreater(Rbnd[0], Rbnd[1])

        logR = np.flipud(logR)

        Rbnd = StoneRbnd(StoneVgrid(np.power(10, logR), Ka, gnu, Kx, L0))

        self.assertGreater(Rbnd[1], Rbnd[0])

        logR[0:2] = 2.0

        Ka[0:2] = [1E4, 1E5]

        Rbnd = StoneRbnd(StoneVgrid(np.power(10, logR), Ka, gnu, Kx, L0))

        self.assertGreater(Rbnd[1], Rbnd[0])

    def retReqDebug(self, logR, Ka):
        gnu = 10
        Kx = 1E-5
        L0 = 1E-5

        output = reqSolver(logR, Ka, gnu, Kx, L0)

        vGrid = StoneVgrid(np.power(10, output), Ka, gnu, Kx, L0)

        Rbnd = StoneRbnd(vGrid)

        Rtot = np.power(10, output) + Rbnd

        deltaR = np.linalg.norm(Rtot - np.power(10, logR))

        self.assertAlmostEqual(deltaR, 0.0, delta=0.1, msg="Mass balance failed on reqSolver")

        return (output, vGrid, Rbnd)

    def test_reqSolver(self):
        """ Run various tests to verify reqSolver function. """

        logR = np.array([5, 5], dtype=np.float64)
        Ka = np.array([1E5, 1E4], dtype=np.float64)

        output, _, _ = self.retReqDebug(logR, Ka)
        self.assertGreater(output[1], output[0])

        # Flip Ka around and see the relationship still applies
        Ka[0:2] = [1.0E2, 1.0E6]
        output, _, _ = self.retReqDebug(logR, Ka)
        self.assertGreater(output[0], output[1])

        # Now keep Ka equal but have asymmetric expression
        Ka[0:2] = 1.0E5
        logR[0:2] = [4.0, 5.0]
        output, _, _ = self.retReqDebug(logR, Ka)
        self.assertGreater(output[1], output[0])

        # And perform same with expression switched
        logR[0:2] = [5.0, 4.0]
        output, _, _ = self.retReqDebug(logR, Ka)
        self.assertGreater(output[0], output[1])

    def test_all(self):
        logR = np.array([5, 5, 5, 5], dtype=np.float64)
        Ka = np.array([1E5, 1E4, 1E5, 1E5], dtype=np.float64)
        Kx = np.power(10, -12.5)
        gnu = 4
        L0 = 1E-9

        StoneN(logR, Ka, Kx, gnu, L0)

        Ka = np.array([1E5, 1E6, 1E5, 1E5], dtype=np.float64)

        StoneN(logR, Ka, Kx, gnu, L0)

        Ka = np.array([1E5, 1E5, 1E5, 1E5], dtype=np.float64)

        cc = StoneN(logR, Ka, Kx, gnu, L0)

        rmulti = cc.getRmultiAll()
        rbnd = cc.getRbnd()

        for ii in range(4):
            self.assertTrue(np.isclose(rmulti[0], rmulti[ii]))
            self.assertTrue(np.isclose(rbnd[0], rbnd[ii]))

    def test_activity(self):
        """
        This test reduces the affinity of a low abundance receptor and makes sure there aren't changes.
        It sets all combinations of one and two receptors to low expression, then changes those receptor
        affinities.
        """

        Kx = np.power(10, -12.5)
        gnu = 4
        L0 = 1E-9
        activity = [1, -1, 1, 1]

        for ii in list(itertools.combinations(range(4), 2)) + list(range(4)):
            logR = np.full((4,), 3, dtype=np.float64)
            logR[np.array(ii)] = -6
            Ka = np.array([1E5, 1E4, 1E5, 1E5], dtype=np.float64)

            one = StoneN(logR, Ka, Kx, gnu, L0).getActivity(activity)

            Ka[np.array(ii)] = 1E-6

            self.assertTrue(np.isclose(one,
                                       StoneN(logR, Ka, Kx, gnu, L0).getActivity(activity)))

    def test_simplify_to_monovalent(self):
        """ Check that the generalized multi-receptor model simplifies to
        Stone's model in the case of single-receptor expression """
        from ..StoneModel import StoneMod
        Kx = np.power(10, -12.5)
        gnu = 4
        L0 = 1e-9

        for Kaa in [np.float(j) for j in range(3, 10)]:
            logR = np.array([3.0], dtype=np.float64)
            Ka = np.array([Kaa], dtype=np.float64)

            cc = StoneN(logR, Ka, Kx, gnu, L0)
            multi = (cc.getLbnd(), cc.getRbnd(), cc.getRmultiAll())
            mono = StoneMod(logR[0], Ka[0], gnu, Ka[0] * Kx, L0)
            for j in range(3):
                if j == 0:
                    self.assertTrue(np.isclose(multi[j], mono[j]))
                else:
                    self.assertTrue(np.isclose(multi[j][0], mono[j]))


if __name__ == '__main__':
    unittest.main()
