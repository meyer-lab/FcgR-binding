import unittest
import time
import numpy as np
from ..StoneTwoRecep import StoneVgrid, StoneRmultiAll, nmultichoosek, reqSolver, StoneRbnd

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

    # Test that varying Req and Ka provides the expected results
    def test_vGridVar(self):
        Req = np.array([1E4, 1E3], dtype = np.float64)
        Ka = np.array([1E3, 1E3], dtype = np.float64)
        L0 = 1.000E-7
        Kx = 1.0E-5
        gnu = 4

        output = StoneVgrid(Req,Ka,gnu,Kx,L0)
        self.assertGreater(output[3,0], output[0,3])

        Req = np.flipud(Req)
        output = StoneVgrid(Req,Ka,gnu,Kx,L0)
        self.assertLess(output[3,0], output[0,3])

        Req[0:2] = [1E3, 1E3]
        Ka[0:2] = [1E4, 1E3]

        output = StoneVgrid(Req,Ka,gnu,Kx,L0)
        self.assertGreater(output[3,0], output[0,3])

        Ka = np.flipud(Ka)
        output = StoneVgrid(Req,Ka,gnu,Kx,L0)
        self.assertLess(output[3,0], output[0,3])

    def test_StoneRbnd(self):
        gnu = 4

        vGrid = np.ones([gnu+1, gnu+1], dtype = np.float64)
        vGrid[0,0] = 0

        for ii in range(vGrid.shape[0]):
            for jj in range(vGrid.shape[0]):
                if ii+jj > gnu:
                    vGrid[ii,jj] = 0

        output = StoneRbnd(vGrid)
        outputmulti = StoneRmultiAll(vGrid)

        self.assertEqual(output[0], 20)
        self.assertEqual(output[1], 20)
        self.assertEqual(outputmulti[0], 19)
        self.assertEqual(outputmulti[1], 19)

        vGrid[2,0] = 2

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

        Rbnd = StoneRbnd(StoneVgrid(np.power(10,logR),Ka,gnu,Kx,L0))

        self.assertGreater(Rbnd[0], Rbnd[1])

        logR = np.flipud(logR)

        Rbnd = StoneRbnd(StoneVgrid(np.power(10,logR),Ka,gnu,Kx,L0))

        self.assertGreater(Rbnd[1], Rbnd[0])


        logR[0:2] = 2.0

        Ka[0:2] = [1E4, 1E5]

        Rbnd = StoneRbnd(StoneVgrid(np.power(10,logR),Ka,gnu,Kx,L0))

        self.assertGreater(Rbnd[1], Rbnd[0])

    def retReqDebug(self, logR, Ka):
        gnu = 10
        Kx = 1E-5
        L0 = 1E-5

        output = reqSolver(logR,Ka,gnu,Kx,L0)

        vGrid = StoneVgrid(np.power(10,output),Ka,gnu,Kx,L0)

        Rbnd = StoneRbnd(vGrid)

        Rtot = np.power(10,output) + Rbnd

        deltaR = np.linalg.norm(Rtot - np.power(10,logR))

        self.assertAlmostEqual(deltaR, 0.0, delta = 0.1, msg = "Mass balance failed on reqSolver")

        return (output, vGrid, Rbnd)

    def test_reqSolver(self):
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

if __name__ == '__main__':
    unittest.main()
