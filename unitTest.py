import unittest
import StoneModel
import numpy as np

class TestStoneMethods(unittest.TestCase):
    def setUp(self):
        self.M = StoneModel.StoneModel()

    def test_StoneMod(self):
        biCoefMat = self.M.data['biCoefMat']
        tnpbsa = self.M.data['tnpbsa']
        L0 = tnpbsa[0]

        go = 0
        while go < 10:
            R = 50000*np.random.rand(1)
            logR = np.log10(R)
            Ka = 10**(np.random.rand(1)+5)
            logKx = 8*np.random.rand(1)-12
            v = np.random.randint(1,30)

            temp = self.M.StoneMod(logR,Ka,v,logKx,L0,biCoefMat)
            # Ideally write an assertion for accuracy here.
            go += 1

    def test_pseudoNormLike(self):
        print("Testing pseudoNormlike")

    def test_NormalErrorCoef(self):
        data = self.M.data

        print(self.M.NormalErrorCoef([1]*12, data['kaBruhns'], data['mfiAdjMean'], data['tnpbsa'], data['meanPerCond'], data['biCoefMat']))
        print(self.M.StoneMod(8,1e-6,4,-8,7e-6,self.M.biCoefMat))









if __name__ == '__main__':
    unittest.main()
