"unit test for the Vec2D class"

import unittest

from molly.Vec2D import Vec2D, orientation

class Vec2DTest(unittest.TestCase):
    "test class"

    def test_default_constructor(self):
        "test default constructor"
        vec = Vec2D()
        self.assertEqual(0.0, vec.pos_x)
        self.assertEqual(0.0, vec.pos_y)



if __name__ == "__main__":
    unittest.main()
