"unit tests for Tangent class"

import unittest

from molly.Tangent import Tangent
from molly.Circle import Circle
from molly.Vec2D import Vec2D

class TangentTest(unittest.TestCase):
    "test class"

    def test_constructor(self):
        "test constructor"
        start_pos = Vec2D(0, 1)
        start_circ = Circle()
        start_orient = 1
        end_pos = Vec2D(2, 1)
        end_circ = Circle(Vec2D(2, 0))
        end_orient = -1

        tan = Tangent(start_pos,
                      start_circ,
                      start_orient,
                      end_pos,
                      end_circ,
                      end_orient)
        self.assertTrue(tan.start_pos == start_pos)
        self.assertTrue(tan.start_pos == start_pos)
        self.assertTrue(tan.start_circle == start_circ)
        self.assertTrue(tan.end_orient == end_orient)
        self.assertTrue(tan.end_circle == end_circ)
        self.assertTrue(tan.end_orient == end_orient)

    def test_simple_intersection(self):
        "test simple 1 point intersection"
        tan1 = Tangent(Vec2D(-1, 0), None, None, Vec2D(1, 0), None, None)
        tan2 = Tangent(Vec2D(0, -1), None, None, Vec2D(0, 1), None, None)

        self.assertTrue(tan1.intersect(tan2))
        self.assertTrue(tan2.intersect(tan1))

    def test_overlapping_intersection(self):
        "test that overlapping counts as intersection"
        tan1 = Tangent(Vec2D(-1, 0), None, None, Vec2D(1, 0), None, None)
        tan2 = Tangent(Vec2D(-2, 0), None, None, Vec2D(0, 0), None, None)

        self.assertTrue(tan1.intersect(tan2))
        self.assertTrue(tan2.intersect(tan1))

    def test_colinear_nonoverlapping(self):
        "test that colinear nonoverlapping doesn't count as intersection"
        tan1 = Tangent(Vec2D(1, 0), None, None, Vec2D(2, 0), None, None)
        tan2 = Tangent(Vec2D(-2, 0), None, None, Vec2D(0, 0), None, None)

        self.assertFalse(tan1.intersect(tan2))
        self.assertFalse(tan2.intersect(tan1))

    def test_parallel_intersection(self):
        "test that parallel segments don't intersect"
        tan1 = Tangent(Vec2D(1, 0), None, None, Vec2D(2, 0), None, None)
        tan2 = Tangent(Vec2D(1, 1), None, None, Vec2D(2, 1), None, None)

        self.assertFalse(tan1.intersect(tan2))
        self.assertFalse(tan2.intersect(tan1))

    def test_general_intersection(self):
        "test non intersecting segments"
        tan1 = Tangent(Vec2D(1, 0), None, None, Vec2D(2, 0), None, None)
        tan2 = Tangent(Vec2D(0, -2), None, None, Vec2D(0, -1), None, None)

        self.assertFalse(tan1.intersect(tan2))
        self.assertFalse(tan2.intersect(tan1))

    # intersection with circle is tested in unittest for circle class

if __name__ == "__main__":
    unittest.main()
