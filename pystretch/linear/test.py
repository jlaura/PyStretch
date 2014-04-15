import unittest
import numpy as np

import Linear as lin

import pystretch.core.globalarr




class TestSTD(unittest.TestCase):
    def setUp(self):
        np.random.seed(10)
        glb.sharedarray = np.random.random(100).reshape(10, 10)

        self.kwargs = {}
        self.kwargs['maximum'] = np.amax(glb.sharedarray)
        self.kwargs['mean'] = np.mean(glb.sharedarray)
        self.kwargs['standard_deviation'] = np.std(glb.sharedarray)
        self.kwargs['sigma'] = 2.0
        self.kwargs['ndv'] = 0.0

    def test(self):
        print glb.sharedarray
        lin.standard_deviation_stretch(None, self.kwargs)
        print glb.sharedarray


if __name__ == '__main__':
    unittest.main()
