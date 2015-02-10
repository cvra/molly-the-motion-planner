"basic circle functionality"

from molly.Vec2D import Vec2D
from molly.Tangent import Tangent
from math import sqrt

class Circle(object):
    "simple 2d circle class"

    def __init__(self, pos=Vec2D(), radius=1.0):
        self.pos = pos
        self.radius = radius

    def intersects(self, other):
        "return if self intersects other circle"
        return (self.pos - other.pos).length() <= (self.radius + other.radius)

    def contains_circle(self, other):
        "return if self contains other circle"
        return (self.pos - other.pos).length() <= (self.radius - other.radius)

    def contains_point(self, point):
        "return if self contains point"
        return (self.pos - point).length() <= self.radius

    def tangent_circle(self, circle):
        "tangents between self and other circle"
        if self.contains_circle(circle) or circle.contains_circle(self):
            return []

        tans = self._outertangents(circle)

        if not self.intersects(circle):
            inner = self._innertangents(circle)

            for tan in inner:
                tans.append(tan)

        return tans

    def tangent_polygon(self, poly):
        "tangent between self and polygon"
        return poly.tangent_circle(self)

    def _innertangents(self, other):
        "helper function: compute inner pair of tangents"
        return self._circle_tangents(other, True)

    def _outertangents(self, other):
        "helper function: compute outer pair of tangents"
        return self._circle_tangents(other, False)

    def _circle_tangents(self, other, invert_second_radius):
        "compute tangents as explained in \
        https://en.wikipedia.org/wiki/Tangent_lines_to_circles#Analytic_geometry"

        dx = other.pos.pos_x - self.pos.pos_x
        dy = other.pos.pos_y - self.pos.pos_y
        if not invert_second_radius:
            dr = other.radius - self.radius
        else:
            dr = - other.radius - self.radius
        d = sqrt(dx*dx + dy*dy)

        x = dx/d
        y = dy/d
        r = dr/d

        a1 = r*x - y*sqrt(1 - r*r)
        b1 = r*y + x*sqrt(1 - r*r)
        c1 = self.radius - (a1*self.pos.pos_x + b1*self.pos.pos_y)

        a2 = r*x + y*sqrt(1 - r*r)
        b2 = r*y - x*sqrt(1 - r*r)
        c2 = self.radius - (a2*self.pos.pos_x + b2*self.pos.pos_y)

        x11 = (b1*(b1*self.pos.pos_x - a1*self.pos.pos_y) - a1*c1)
        y11 = (a1*(-b1*self.pos.pos_x + a1*self.pos.pos_y) - b1*c1)

        x12 = (b1*(b1*other.pos.pos_x - a1*other.pos.pos_y) - a1*c1)
        y12 = (a1*(-b1*other.pos.pos_x + a1*other.pos.pos_y) - b1*c1)

        x21 = (b2*(b2*self.pos.pos_x - a2*self.pos.pos_y) - a2*c2)
        y21 = (a2*(-b2*self.pos.pos_x + a2*self.pos.pos_y) - b2*c2)

        x22 = (b2*(b2*other.pos.pos_x - a2*other.pos.pos_y) - a2*c2)
        y22 = (a2*(-b2*other.pos.pos_x + a2*other.pos.pos_y) - b2*c2)

        start1 = Vec2D(x11, y11)
        end1 = Vec2D(x12, y12)
        orient11 = Vec2D.orientation(end1, start1, self.pos)
        orient12 = Vec2D.orientation(start1, end1, other.pos)

        start2 = Vec2D(x21, y21)
        end2 = Vec2D(x22, y22)
        orient21 = Vec2D.orientation(end2, start2, self.pos)
        orient22 = Vec2D.orientation(start2, end2, other.pos)

        tan1 = Tangent(start1, self, orient11, end1, other, orient12)
        tan2 = Tangent(start2, self, orient21, end2, other, orient22)

        return [tan1, tan2]

    def intersects_tangent(self, tangent):
        "return whether self intersects with tangent"

        if self == tangent.start_circle or self == tangent.end_circle:
            return False

        direction = tangent.end_pos - tangent.start_pos
        diff = tangent.start_pos - self.pos

        param1 = direction.dot(direction)
        param2 = 2 * direction.dot(diff)
        param3 = diff.dot(diff) - (self.radius * self.radius)

        for res in Circle.solve_quadratic(param1, param2, param3):
            if res >= 0 and res <= 1:
                return True
        return False

    def __str__(self):
        "string representation for debugging"
        return "Circle: {pos}, {r}".format(pos=str(self.pos), r=self.radius)

    def __add__(self, vec):
        "translate circle by vec"
        return Circle(self.pos + vec, self.radius)

    def __eq__(self, other):
        "two circles are equal if the have the same center position and radius"

        if other is None:
            return False

        return (self.pos == other.pos and
                abs(self.radius - other.radius) < Vec2D.EPSILON)

    def __ne__(self, other):
        "complement of equals"
        return not self == other

    @staticmethod
    def solve_quadratic(param_a, param_b, param_c):
        "solve a*x^2 + b*x + c = 0"
        det = param_b*param_b - 4*param_a*param_c

        if det < 0:
            return []
        elif abs(det) < Vec2D.EPSILON:
            return [-param_b/(2*param_a)]
        else:
            sqrt_det = sqrt(det)
            res1 = (-param_b + sqrt_det)/(2 * param_a)
            res2 = (-param_b - sqrt_det)/(2 * param_a)
            return [res1, res2]
