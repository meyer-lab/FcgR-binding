import unittest
import time
from ..ValidationOrtiz import Ortiz

class TestOrtizMethods(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()
        self.Ortiz = Ortiz()

    def tearDown(self):
        t = time.time() - self.startTime
        print("%s: %.3f" % (self.id(), t*1000))

if __name__ == '__main__':
    unittest.main()
