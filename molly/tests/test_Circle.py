"unit tests for Circle class"

import unittest

from molly.Vec2D import Vec2D
from molly.Circle import Circle
from molly.Tangent import Tangent

from math import asin, sqrt

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

    def test_quadratic_no_solutions(self):
        "test result of unsatisfiable quadratic equation"
        result = Circle.solve_quadratic(1, 0, 1)
        self.assertTrue(len(result) == 0)

    def test_quadratic_single_solution(self):
        "test result of quadratic equation with unique solution"
        result = Circle.solve_quadratic(1, 2, 1)
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0] == -1)

    def test_quadratic_two_solutions(self):
        "test result of quadratic equation with two solutions"
        results = Circle.solve_quadratic(1, -3, 2)
        self.assertTrue(len(results) == 2)

        verify_results = all(res == 1 or res == 2 for res in results)
        self.assertTrue(verify_results)

    def test_intersecting_tangent(self):
        "test single intersection point"
        circle = Circle()
        tangent = Tangent(Vec2D(), None, None, Vec2D(0, 2), None, None)

        self.assertTrue(circle.intersects_tangent(tangent))

    def test_fullintersection_tangent(self):
        "test 2 intersection points"
        circle = Circle()
        tangent = Tangent(Vec2D(0, -2), None, None, Vec2D(0, 2), None, None)

        self.assertTrue(circle.intersects_tangent(tangent))

    def test_contains_tangent(self):
        "test start and end inside circle"
        circle = Circle()
        tangent = Tangent(Vec2D(0, -0.5), None, None, Vec2D(0, 0.5), None, None)

        self.assertFalse(circle.intersects_tangent(tangent))

    def test_touching_tangent(self):
        "test start and end inside circle"
        circle = Circle()
        tangent = Tangent(Vec2D(0, 1), None, None, Vec2D(0, 2), None, None)

        self.assertTrue(circle.intersects_tangent(tangent))

    def test_self_tangent(self):
        "test if tangent is part of circle"
        circle1 = Circle()
        circle2 = Circle(Vec2D(0, 2), 1)
        tan = Tangent(Vec2D(0, 1), circle1, None, Vec2D(0, 2), circle2, None)

        self.assertFalse(circle1.intersects_tangent(tan))
        self.assertFalse(circle2.intersects_tangent(tan))

    def test_nonintersecting_tangent(self):
        "test intersection with nonintersecting tangent"
        circle = Circle()
        tan = Tangent(Vec2D(10, 10), None, None, Vec2D(11, 11), None, None)

        self.assertFalse(circle.intersects_tangent(tan))

    def test_tangents_containing_circle(self):
        "test circle tangents when one circle contains another"
        circle1 = Circle(Vec2D(), 10)
        circle2 = Circle(Vec2D(), 5)

        self.assertTrue(len(circle1.tangent_circle(circle2)) == 0)
        self.assertTrue(len(circle2.tangent_circle(circle1)) == 0)

    def test_tangents_intersec_circles(self):
        "test circle tangents of intersecting circles"
        circle1 = Circle(Vec2D(), 2)
        circle2 = Circle(Vec2D(3, 0), 2)

        tans = circle1.tangent_circle(circle2)

        self.assertTrue(len(tans) == 2)

        tan1 = Tangent(Vec2D(0, 2), circle1, 1, Vec2D(3, 2), circle2, -1)
        tan2 = Tangent(Vec2D(0, -2), circle1, -1, Vec2D(3, -2), circle2, 1)

        verify = all(tan == tan1 or tan == tan2 for tan in tans)

        self.assertTrue(verify)

    def test_circle_tangents_full(self):
        "test tangents between two disjoint circles"

        circ1 = Circle()
        circ2 = Circle(Vec2D(4, 0))

        midpoint = Vec2D(2, 0)

        hypothenuse = (midpoint - circ1.pos).length()
        opp_side = circ1.radius

        tan_len = sqrt(hypothenuse * hypothenuse - opp_side * opp_side)

        angle = asin(opp_side / hypothenuse)

        start1 = (circ1.pos - midpoint).rotate(angle).normalized() * tan_len
        start1 = start1 + midpoint
        end1 = (circ2.pos - midpoint).rotate(angle).normalized() * tan_len
        end1 = end1 + midpoint

        start2 = (circ1.pos - midpoint).rotate(-angle).normalized() * tan_len
        start2 = start2 + midpoint
        end2 = (circ2.pos - midpoint).rotate(-angle).normalized() * tan_len
        end2 = end2 + midpoint

        r_tans = []
        r_tans.append(Tangent(start1, circ1, -1, end1, circ2, -1))
        r_tans.append(Tangent(start2, circ1, 1, end2, circ2, 1))
        r_tans.append(Tangent(Vec2D(0, 1), circ1, 1, Vec2D(4, 1), circ2, -1))
        r_tans.append(Tangent(Vec2D(0, -1), circ1, -1, Vec2D(4, -1), circ2, 1))

        tans = circ1.tangent_circle(circ2)

        self.assertTrue(len(tans) == 4)

        valid = all(t in r_tans for t in tans)

        self.assertTrue(valid)

    # polygon tangents tested in unittest for polygon class


if __name__ == "__main__":
    unittest.main()
