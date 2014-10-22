"unit tests for Circle class"

import unittest

from molly.Vec2D import Vec2D
from molly.Circle import Circle

class CircleTest(unittest.TestCase):
    "test class for circles"

    def test_default_constructor(self):
        "default constructor should return unit circle"

        circle = Circle()

        self.assertTrue(circle.pos == Vec2D())
        self.assertAlmostEqual(circle.radius, 1.0)

    def test_standard_constructor(self):
        "test that class members are correctly set on construction"

        center = Vec2D(1, 2)
        radius = 1.2

        circle = Circle(center, radius)

        self.assertTrue(circle.pos == center)
        self.assertAlmostEqual(radius, circle.radius)

    def test_circle_circle_intersection(self):
        "test intersection of intersecting circles"

        circ1 = Circle()
        circ2 = Circle(Vec2D(0.5, 0))

        self.assertTrue(circ1.intersects(circ2))
        self.assertTrue(circ2.intersects(circ1))

    def test_not_intersecting_circles(self):
        "test intersection of not intersecting circles"

        circ1 = Circle()
        circ2 = Circle(Vec2D(10, 0))

        self.assertFalse(circ1.intersects(circ2))
        self.assertFalse(circ2.intersects(circ1))

    def test_intersection_equal_circles(self):
        "test intersection of equal circles"

        circ1 = Circle()
        circ2 = Circle()

        self.assertTrue(circ1.intersects(circ2))
        self.assertTrue(circ2.intersects(circ1))

    def test_touching_intersection(self):
        "test intersection of tangent circles"

        circ1 = Circle()
        circ2 = Circle(Vec2D(1, 0))

        self.assertTrue(circ1.intersects(circ2))
        self.assertTrue(circ2.intersects(circ1))

    def test_containing_circles(self):
        "test circle containment"

        circ1 = Circle()
        circ2 = Circle(Vec2D(), 0.5)

        self.assertTrue(circ1.contains_circle(circ2))
        self.assertFalse(circ2.contains_circle(circ1))

    def test_contains_impl_intersects(self):
        "containment implies intersection"

        circ1 = Circle()
        circ2 = Circle(Vec2D(), 0.5)

        self.assertTrue(circ1.contains_circle(circ2))
        self.assertTrue(circ1.intersects(circ2))
        self.assertTrue(circ2.intersects(circ1))

    def test_containment_equal_circles(self):
        "if two circles are equal one contains the other and vice versa"

        circ1 = Circle()
        circ2 = Circle()

        self.assertTrue(circ1.contains_circle(circ2))
        self.assertTrue(circ2.contains_circle(circ1))

    def test_point_containment(self):
        "test point inside circle"

        point = Vec2D()
        circle = Circle()

        self.assertTrue(circle.contains_point(point))

    def test_point_not_inside(self):
        "test point not inside circle"

        point = Vec2D(2, 0)
        circle = Circle()

        self.assertFalse(circle.contains_point(point))

    def test_point_on_border(self):
        "test point exactly on circle border"

        point = Vec2D(1, 0)
        circle = Circle()

        self.assertTrue(circle.contains_point(point))

    def test_translation(self):
        "test translating circle by some vector"

        trans = Vec2D(1, 0)
        circle = Circle()

        translated = circle + trans

        self.assertTrue(translated.pos == circle.pos + trans)
        self.assertAlmostEqual(translated.radius, circle.radius)

    def test_equality(self):
        "test equality (and implicitely non-equality) of cirlces"

        circle1 = Circle(Vec2D(1, 0), 1.0)
        circle2 = Circle(
            Vec2D(1, 0.9 * Vec2D.EPSILON),
            1.0 + 0.9 * Vec2D.EPSILON)

        self.assertTrue(circle1 == circle2)
        self.assertTrue(circle2 == circle1)
        # equality is symmetric
        self.assertFalse(circle1 != circle2)
        self.assertFalse(circle2 != circle1)
