import unittest
import random
import time
from ..StoneTwoRecep import *

class TestStoneTwoRecpMethods(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t*1000))

    def test_nmultichoosek(self):
        # Check that the case with avidity 2 works as expected
        self.assertTrue(nmultichoosek(2,0,0) == 1)
        self.assertTrue(nmultichoosek(2,1,0) == 2)
        self.assertTrue(nmultichoosek(2,0,1) == 2)
        self.assertTrue(nmultichoosek(2,2,0) == 1)
        self.assertTrue(nmultichoosek(2,0,2) == 1)
        self.assertTrue(nmultichoosek(2,1,1) == 2)

        # Check that avidity 3 works
        self.assertTrue(nmultichoosek(3,0,0) == 1)
        self.assertTrue(nmultichoosek(3,1,0) == 3)
        self.assertTrue(nmultichoosek(3,0,1) == 3)
        self.assertTrue(nmultichoosek(3,2,0) == 3)
        self.assertTrue(nmultichoosek(3,0,2) == 3)
        self.assertTrue(nmultichoosek(3,1,1) == 6)

        # Check that avidity 4 works
        self.assertTrue(nmultichoosek(4,1,1) == 12)
        self.assertTrue(nmultichoosek(4,3,1) == 4)
        self.assertTrue(nmultichoosek(4,1,3) == 4)
        self.assertTrue(nmultichoosek(4,2,1) == 12)
        self.assertTrue(nmultichoosek(4,1,2) == 12)
        self.assertTrue(nmultichoosek(4,2,2) == 6)

    def test_StoneVgrid(self):
        Req = np.array([1000, 1000], dtype = np.float64)
        Ka = np.array([1000, 2000], dtype = np.float64)
        L0 = 1.000E-7
        Kx = 1.0E-5
        gnu = 4

        output = StoneVgrid(Req,Ka,gnu,Kx,L0)

        # Check that the grid is setup appropriately
        for ii in range(gnu+1):
            for jj in range(gnu+1):
                if ii+jj > gnu:
                    self.assertEqual(output[ii,jj], 0)
                elif ii == 0 and jj == 0:
                    self.assertEqual(output[ii,jj], 0)
                else:
                    self.assertNotEqual(output[ii,jj], 0)

        # Kx is specified in the reference of the first receptor
        Kx = Ka[1]/Ka[0]*Kx

        # Assemble the grid for the mirror case
        output2 = StoneVgrid(np.flipud(Req),np.flipud(Ka),gnu,Kx,L0)

        # Check that detailed balance holds
        self.assertTrue(np.all(np.equal(output, np.transpose(output2))))


if __name__ == '__main__':
    unittest.main()
