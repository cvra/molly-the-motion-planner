"unit test for the Vec2D class"

import unittest
import math

from molly.Vec2D import Vec2D, orientation

class Vec2DTest(unittest.TestCase):
    "test class"

    def test_default_constructor(self):
        "test default constructor"
        vec = Vec2D()
        self.assertAlmostEqual(0.0, vec.pos_x)
        self.assertAlmostEqual(0.0, vec.pos_y)

    def test_constructor(self):
        "test constructor"
        x_pos = 1.0
        y_pos = 2.0

        vec = Vec2D(x_pos, y_pos)

        self.assertAlmostEqual(x_pos, vec.pos_x)
        self.assertAlmostEqual(y_pos, vec.pos_y)

    def test_dot_product(self):
        "test the dot product of 2 vectors"
        posx1 = 1.0
        posy1 = 2.0
        posx2 = 3.0
        posy2 = 4.0

        vec1 = Vec2D(posx1, posy1)
        vec2 = Vec2D(posx2, posy2)

        expected = posx1 * posx2 + posy1 * posy2

        self.assertAlmostEqual(expected, vec1.dot(vec2))
        # dot product is commutativ
        self.assertAlmostEqual(vec1.dot(vec2), vec2.dot(vec1))

    def test_cross_product(self):
        "test the cross product of 2 vectors"
        posx1 = 1.0
        posy1 = 2.0
        posx2 = 3.0
        posy2 = 4.0

        vec1 = Vec2D(posx1, posy1)
        vec2 = Vec2D(posx2, posy2)

        expected = posx1 * posy2 - posy1 * posx2

        self.assertAlmostEqual(expected, vec1.cross(vec2))
        self.assertAlmostEqual(vec1.cross(vec2), -vec2.cross(vec1))

    def test_length_of_null_vector(self):
        "test correct length of null vector"
        self.assertAlmostEqual(0.0, Vec2D().length())

    def test_length(self):
        "test correct length implementation"

        posx = 5.0
        posy = 10.0

        vec = Vec2D(posx, posy)

        expected = math.sqrt(posx * posx + posy * posy)

        self.assertAlmostEqual(expected, vec.length())

    def test_normalized_of_null_vector(self):
        "cannot normalize null vector"
        with self.assertRaises(ZeroDivisionError):
            Vec2D().normalized()

    def test_normalized_nonunitvector(self):
        "test normal behavior"
        vec = Vec2D(1, 1)

        unit = vec.normalized()

        self.assertAlmostEqual(1, unit.length())
        self.assertAlmostEqual(1.0/math.sqrt(2), unit.pos_x)
        self.assertAlmostEqual(1.0/math.sqrt(2), unit.pos_y)

    def test_normalized_unit_vector(self):
        "normalized unit vector gives same vector"
        vec = Vec2D(1, 0)

        unit = vec.normalized()

        self.assertAlmostEqual(vec.pos_x, unit.pos_x)
        self.assertAlmostEqual(vec.pos_y, unit.pos_y)

    def test_rotate_around_origin(self):
        "rotate around origin"

        vec = Vec2D(1, 0)

        rot = vec.rotate(math.pi/4)
        self.assertAlmostEqual(1.0/math.sqrt(2), rot.pos_x)
        self.assertAlmostEqual(1.0/math.sqrt(2), rot.pos_y)

    def test_rotate_around_point(self):
        "rotate around some point"

        vec = Vec2D()

        center = Vec2D(-1, 0)

        rot = vec.rotate(math.pi/4, center)

        self.assertAlmostEqual(1.0/math.sqrt(2) - 1, rot.pos_x)
        self.assertAlmostEqual(1.0/math.sqrt(2), rot.pos_y)

    def test_unary_minus(self):
        "test unary minus"

        vec = Vec2D(13, 17)
        neg = -vec

        self.assertAlmostEqual(-vec.pos_x, neg.pos_x)
        self.assertAlmostEqual(-vec.pos_y, neg.pos_y)

    def test_vector_addition(self):
        "test vector addition"
        posx1 = 1.0
        posy1 = 2.0
        posx2 = 3.0
        posy2 = 4.0

        vec1 = Vec2D(posx1, posy1)
        vec2 = Vec2D(posx2, posy2)

        res = vec1 + vec2

        self.assertAlmostEqual(posx1 + posx2, res.pos_x)
        self.assertAlmostEqual(posy1 + posy2, res.pos_y)

        # commutatif
        self.assertAlmostEqual((vec1 + vec2).pos_x, (vec2 + vec1).pos_x)
        self.assertAlmostEqual((vec1 + vec2).pos_y, (vec2 + vec1).pos_y)

    def test_vector_subtraction(self):
        "test vector addition"
        posx1 = 1.0
        posy1 = 2.0
        posx2 = 3.0
        posy2 = 4.0

        vec1 = Vec2D(posx1, posy1)
        vec2 = Vec2D(posx2, posy2)

        res = vec1 - vec2

        self.assertAlmostEqual(posx1 - posx2, res.pos_x)
        self.assertAlmostEqual(posy1 - posy2, res.pos_y)

    def test_multiplication_by_scalar(self):
        "multiplication by scalar factor"

        vec = Vec2D(3, 4)
        factor = 0.7

        res = vec * factor

        self.assertAlmostEqual(vec.pos_x * factor, res.pos_x)
        self.assertAlmostEqual(vec.pos_y * factor, res.pos_y)

    def test_trivial_equality(self):
        "each vector should be equal to itself"

        vec = Vec2D(3, 4)

        self.assertTrue(vec == vec)

    def test_approximate_equality(self):
        "vectors within Vec2D.EPSILON distance of each other should count as \
                equal"

        vec = Vec2D(1, 1)

        approx = vec + Vec2D(1, 0) * (0.9 * Vec2D.EPSILON)

        self.assertTrue(vec == approx)
        self.assertFalse(vec != approx)

    def test_positive_orientation(self):
        "test that orientation returns postive value for positively oriented \
                points"
        vec1 = Vec2D(0, 0)
        vec2 = Vec2D(1, 0)
        vec3 = Vec2D(0, 1)

        self.assertTrue(orientation(vec1, vec2, vec3) > 0)

    def test_negative_orientation(self):
        "test that orientation returns postive value for positively oriented \
                points"
        vec1 = Vec2D(0, 0)
        vec2 = Vec2D(0, 1)
        vec3 = Vec2D(1, 0)

        self.assertTrue(orientation(vec1, vec2, vec3) < 0)

    def test_orientation_colinear(self):
        "test that orientation returns (almost) zero for colinear points"

        vec1 = Vec2D(0, 0)
        vec2 = Vec2D(1, 0)
        vec3 = Vec2D(2, 0)

        self.assertAlmostEqual(0, orientation(vec1, vec2, vec3))

if __name__ == "__main__":
    unittest.main()
