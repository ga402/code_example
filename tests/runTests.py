# Basic test functions ... to be expanded. 
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath('src'))
sys.path.insert(0, os.path.abspath('src/utils'))
from utils.contourtools import *
from utils.func import *
from utils.img2df import img2df as img2df


class TestClass(unittest.TestCase):    
    """test class

    Args:
        unittest (_type_): _description_
    """
    def runTest(self):
        xx, yy = np.mgrid[:200, :200]
        circle = (xx - 100) ** 2 + (yy - 100) ** 2
        circle = np.where(circle < (6400 + 60), 1, 0)
        circle = np.expand_dims(circle, axis=0)
        testclass = img2df(circle)
        self.assertEqual(testclass.getDim(), (1, 200,200), "incorrect dim")
            
    


if __name__ == '__main__':
    unittest.main()

