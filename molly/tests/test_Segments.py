"unit test for Segment classes in Pathplanner.py"

import unittest


from molly.Pathplanner import LineSegment
from molly.Pathplanner import CircleSegment
from molly.Circle import Circle
from molly.Vec2D import Vec2D

from math import pi, sqrt

class LineSegmentTest(unittest.TestCase):
    "test class"

    def test_length(self):
        "test length method"
        seg = LineSegment(Vec2D(), Vec2D(1, 0))

        self.assertAlmostEqual(seg.length(), 1)

    def test_tan(self):
        "test tan method"
        seg = LineSegment(Vec2D(), Vec2D(1, 0))

        self.assertTrue(seg.tan(None).is_equal(Vec2D(1, 0)))

    def test_next_pos(self):
        "test next_pos method"
        seg = LineSegment(Vec2D(), Vec2D(1, 0))

        self.assertTrue(seg.next_pos(Vec2D(), 1).is_equal(Vec2D(1, 0)))

    def test_radial_acc(self):
        "test radial_acc method"
        seg = LineSegment(Vec2D(), Vec2D(1, 0))
        self.assertTrue(seg.radial_acc(Vec2D(), 1).is_equal(Vec2D()))



class CircleSegmentTest(unittest.TestCase):
    "test class"

    def test_length(self):
        "test length method"

        circle = Circle()

        inv_rt2 = sqrt(2.0)/2.0

        seg1 = CircleSegment(Vec2D(1, 0), Vec2D(inv_rt2, inv_rt2), circle, 1)
        seg2 = CircleSegment(Vec2D(1, 0), Vec2D(inv_rt2, inv_rt2), circle, -1)

        self.assertAlmostEqual(seg1.length(), pi * 0.25, delta=Vec2D.EPSILON)
        self.assertAlmostEqual(seg2.length(), pi * 1.75, delta=Vec2D.EPSILON)

    def test_tan(self):
        "test tan method"

        circle = Circle()

        seg1 = CircleSegment(Vec2D(1, 0), Vec2D(0, 1), circle, 1)
        seg2 = CircleSegment(Vec2D(1, 0), Vec2D(0, 1), circle, -1)

        self.assertTrue(seg1.tan(Vec2D(1, 0)).is_equal(Vec2D(0, 1)))
        self.assertTrue(seg2.tan(Vec2D(1, 0)).is_equal(Vec2D(0, -1)))

    def test_radial_acc(self):
        "test radial_acc method"

        circle = Circle()
        seg = CircleSegment(Vec2D(1, 0), Vec2D(0, 1), circle, 1)

        self.assertTrue(seg.radial_acc(Vec2D(1, 0), 1).is_equal(Vec2D(-1, 0)))

    def test_next_pos(self):
        "test next_pos method"

        circle = Circle()

        seg = CircleSegment(Vec2D(1, 0), Vec2D(0, 1), circle, 1)

        self.assertTrue(seg.next_pos(Vec2D(1, 0), pi * 0.5).is_equal(Vec2D(0, 1)))

if __name__ == "__main__":
    unittest.main()
