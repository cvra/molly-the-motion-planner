"basic 2D vector geometry"

from math import acos, sqrt, sin, cos, pi

class Vec2D(object):
    " Simple 2D vector class for euclidean geometry "

    EPSILON = 0.0001

    def __init__(self, x=0.0, y=0.0):
        self.pos_x = x
        self.pos_y = y

    def dot(self, other):
        "dot product"
        return self.pos_x * other.pos_x + self.pos_y * other.pos_y

    def cross(self, other):
        "2d cross product"
        return self.pos_x * other.pos_y - self.pos_y * other.pos_x

    def length(self):
        "length of vector"
        return sqrt(self.dot(self))

    def normalized(self):
        "unit vector with same direction as self"
        length = self.length()
        return self * (1/length)

    def rotate(self, angle, center=None):
        "rotate self by angle radians around center"

        if center is None:
            center = Vec2D()

        centered = self - center

        cosine = cos(angle)
        sine = sin(angle)

        new_pos_x = cosine * centered.pos_x - sine * centered.pos_y
        new_pos_y = sine * centered.pos_x + cosine * centered.pos_y

        final = Vec2D(new_pos_x, new_pos_y) + center

        return final

    def oriented_angle(self, other):
        "oriented angle from self to other"

        vec1 = self.normalized()
        vec2 = other.normalized()

        cross_prod = vec1.cross(vec2) # sin(angle)
        dot_prod = vec1.dot(vec2) # cos(angle)

        if dot_prod < -1.0:
            dot_prod = -1.0

        if dot_prod > 1.0:
            dot_prod = 1.0

        if cross_prod > 0:
            angle = acos(dot_prod)
        else:
            angle = -acos(dot_prod)

        if angle < 0:
            angle = angle + 2 * pi

        return angle


    def __neg__(self):
        return Vec2D(-self.pos_x, -self.pos_y)

    def __add__(self, other):
        return Vec2D(self.pos_x + other.pos_x, self.pos_y + other.pos_y)

    def __sub__(self, other):
        return Vec2D(self.pos_x - other.pos_x, self.pos_y - other.pos_y)

    def __mul__(self, other):
        return Vec2D(self.pos_x * other, self.pos_y * other)

    def __str__(self):
        return "({x},{y})".format(x=self.pos_x, y=self.pos_y)

    def is_equal(self, other):
        return (self - other).length() < Vec2D.EPSILON

    @staticmethod
    def orientation(vec1, vec2, vec3):
        "return positive number if the points are mathematically \
         positively oriented negative number for negative orientation \
         and zero for colinear points"
        vec12 = vec2 - vec1
        vec23 = vec3 - vec2
        return vec12.cross(vec23)
