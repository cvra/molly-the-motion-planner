"unit tests for pathplanner subfunctions"

import unittest

import molly.Pathplanner as pp

from molly.Vec2D import Vec2D
from molly.Circle import Circle

from molly.tests.test_Polygon import dummy_polygon

from math import pi

class PathplannerTest(unittest.TestCase):
    "test class"

    def test_start_circles(self):
        "test generation of starting circles"

        pos = Vec2D()
        direction = Vec2D(0, 1)

        pos_circ = Circle(Vec2D(-1, 0), 1)
        neg_circ = Circle(Vec2D(1, 0), 1)

        (test_pos, test_neg) = pp.get_start_circles(pos, direction, 1)

        self.assertTrue(test_pos.is_equal(pos_circ))
        self.assertTrue(test_neg.is_equal(neg_circ))

    def test_all_tangents_simple1(self):
        "test that all_tangents returns all tangents of two circles \
         when only those 2 circles are present"

        circ1 = Circle(Vec2D(-2, 0), 1)
        circ2 = Circle(Vec2D(2, 0), 1)

        tangents = circ1.tangent_circle(circ2)

        to_test = pp.all_tangents([circ1, circ2], [])

        verificator = all(any(map(test.is_equal, tangents)) for test in to_test)

        self.assertTrue(verificator)

    def test_all_tangents_simple2(self):
        "test that all_tangents returns all tangents of a circle \
         and a polygon and additionally all sides of the polygon"

        circ = Circle(Vec2D(4, 4), 1)
        poly = dummy_polygon()

        correct_tans = circ.tangent_polygon(poly) + poly.sides

        to_test = pp.all_tangents([circ], [poly])

        verificator = all(any(map(test.is_equal, correct_tans)) for test in to_test)

        self.assertTrue(verificator)

    # TODO more complex tests for all_tangents

    def test_sort_points_empty(self):
        "test sort_points_on_circle on empty list"

        self.assertTrue(not pp.sort_points_on_circle([], Circle()))

    def test_sort_points_singleelement(self):
        "test sort_points_on_circle one element list"

        sorted_list = pp.sort_points_on_circle([Vec2D(1, 0)], Circle())

        self.assertTrue(len(sorted_list) == 1)
        self.assertTrue(sorted_list[0].is_equal(Vec2D(1, 0)))

    def test_sort_points_general(self):
        "general test on unit circle"

        point1 = Vec2D(1, 0)
        point2 = point1.rotate(pi/2)
        point3 = point1.rotate(pi)
        point4 = point1.rotate(-pi/2)

        unsorted = [point2, point4, point3, point1]

        to_test = pp.sort_points_on_circle(unsorted, Circle())

        self.assertTrue(len(to_test) == 4)
        self.assertTrue(to_test[0].is_equal(point2))
        self.assertTrue(to_test[1].is_equal(point3))
        self.assertTrue(to_test[2].is_equal(point4))
        self.assertTrue(to_test[3].is_equal(point1))

    def test_neighs_circle_one_element(self):
        "single point has no neighbours"

        points = [Vec2D(1, 0)]

        circle = Circle()

        (pos, neg) = pp.neighbours_on_circle(points, circle, Vec2D(1, 0))

        self.assertTrue(pos is None)
        self.assertTrue(neg is None)

    def test_neighs_circle_two_elements(self):
        "point has only one neighbour"

        point1 = Vec2D(1, 0)
        point2 = point1.rotate(pi/2)

        points = [point1, point2]

        (pos, neg) = pp.neighbours_on_circle(points, Circle(), point1)

        self.assertTrue(pos.is_equal(point2))
        self.assertTrue(neg.is_equal(point2))


    def test_neighs_circle_general(self):
        "point has two distinct neighbours"

        point1 = Vec2D(1, 0)
        point2 = point1.rotate(pi/2)
        point3 = point1.rotate(pi)
        point4 = point1.rotate(-pi/2)

        unsorted = [point2, point4, point3, point1]

        (pos, neg) = pp.neighbours_on_circle(unsorted, Circle(), Vec2D(1, 0))

        self.assertTrue(pos.is_equal(point2))
        self.assertTrue(neg.is_equal(point4))




if __name__ == "__main__":
    unittest.main()
