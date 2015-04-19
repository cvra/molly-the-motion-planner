"unit test for Polygon class"

import unittest

from molly.Polygon import Polygon
from molly.Circle import Circle
from molly.Tangent import Tangent
from molly.Vec2D import Vec2D
from math import sqrt

class PolygonTest(unittest.TestCase):
    "test class"

    def test_translate_zero(self):
        "test translating polygon by zero vector"

        dummy = dummy_polygon()

        translated = dummy + Vec2D()

        self.assertTrue(translated == dummy)
        self.assertTrue(dummy == translated)

    def test_translate_nonzero(self):
        "test translating polygon by nonzero vector"

        dummy = dummy_polygon()

        translation = Vec2D(1, 0)

        translated = dummy + translation

        trans_dummy = translated_dummy(translation)

        self.assertTrue(translated == trans_dummy)
        self.assertTrue(trans_dummy == translated)

    def test_polycircle_intersection(self):
        "test intersection between polygon and circle"

        dummy = dummy_polygon()

        circ = Circle(Vec2D(4, 4))

        tan1 = Tangent(Vec2D(4, 5),
                       Circle(Vec2D(4, 4)),
                       -1,
                       Vec2D(0, 5),
                       Circle(Vec2D(0, 4)),
                       1)
        tan2 = Tangent(Vec2D(5, 4),
                       Circle(Vec2D(4, 4)),
                       1,
                       Vec2D(5, 0),
                       Circle(Vec2D(4, 0)),
                       -1)

        tans = dummy.tangent_circle(circ)

        self.assertTrue(tan1 in tans and tan2 in tans)

        # TODO verify other 2 tangents

    # TODO test polygon to polygon tangents

    @unittest.expectedFailure
    def test_polygon_from_circles_bad1(self):
        Polygon([])

    @unittest.expectedFailure
    def test_polygon_from_circles_bad2(self):
        Polygon([Circle()])

    def test_polygon_from_circles_normal(self):

        ref = dummy_polygon()

        poly = Polygon(ref.corners)

        self.assertTrue(len(ref.corners) == len(poly.corners))

        for ref_corner in ref.corners:
            self.assertTrue(ref_corner in poly.corners)

        self.assertTrue(len(ref.sides) == len(poly.sides))

        for ref_side in ref.sides:
            self.assertTrue(ref_side in poly.sides)


def dummy_polygon():
    "return a dummy triangular polygon"

    circ1 = Circle()
    circ2 = Circle(Vec2D(4, 0))
    circ3 = Circle(Vec2D(0, 4))

    side2_helper = Vec2D(sqrt(2.0)/2.0, sqrt(2.0)/2.0)
    side2_pos1 = circ2.pos + side2_helper
    side2_pos2 = circ3.pos + side2_helper

    side1 = Tangent(Vec2D(0, -1), circ1, -1, Vec2D(4, -1), circ2, 1)
    side2 = Tangent(side2_pos1, circ2, -1, side2_pos2, circ3, 1)
    side3 = Tangent(Vec2D(-1, 4), circ3, -1, Vec2D(-1, 0), circ1, 1)

    return Polygon([circ1, circ2, circ3], [side1, side2, side3])

def translated_dummy(vec):
    "return dummy triangular polygon manually translated by vec"

    delta_x = vec.pos_x
    delta_y = vec.pos_y

    circ1 = Circle(Vec2D(delta_x, delta_y))
    circ2 = Circle(Vec2D(4 + delta_x, 0 + delta_y))
    circ3 = Circle(Vec2D(0 + delta_x, 4 + delta_y))

    side2_helper = Vec2D(sqrt(2.0)/2.0, sqrt(2.0)/2.0)
    side2_pos1 = circ2.pos + side2_helper
    side2_pos2 = circ3.pos + side2_helper

    side1 = Tangent(Vec2D(0 + delta_x, -1 + delta_y),
                    circ1,
                    -1,
                    Vec2D(4 + delta_x, -1 + delta_y),
                    circ2,
                    1)
    side2 = Tangent(side2_pos1, circ2, -1, side2_pos2, circ3, 1)
    side3 = Tangent(Vec2D(-1 + delta_x, 4 + delta_y),
                    circ3,
                    -1,
                    Vec2D(-1 + delta_x, 0 + delta_y),
                    circ1,
                    1)
    return Polygon([circ1, circ2, circ3], [side1, side2, side3])


if __name__ == "__main__":
    unittest.main()
