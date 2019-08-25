import unittest
import numpy as np
from ..StoneNRecep import StoneN


class TestStoneNRecpMethods(unittest.TestCase):

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
            mono = StoneMod(logR[0], Ka[0], gnu, Ka[0] * Kx, L0, fullOutput=True)
            for j in range(3):
                if j == 0:
                    self.assertTrue(np.isclose(multi[j], mono[j]))
                else:
                    self.assertTrue(np.isclose(multi[j][0], mono[j]))


if __name__ == '__main__':
    unittest.main()
