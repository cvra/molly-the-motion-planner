"basic circle functionality"

from molly.Vec2D import Vec2D

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

    def __str__(self):
        "string representation for debugging"
        return "Circle: {pos}, {r}".format(pos=str(self.pos), r=self.radius)

    def __add__(self, vec):
        "translate circle by vec"
        return Circle(self.pos + vec, self.radius)

    def __eq__(self, other):
        "two circles are equal if the have the same center position and radius"
        return (self.pos == other.pos and
                abs(self.radius - other.radius) < Vec2D.EPSILON)

    def __ne__(self, other):
        "complement of equals"
        return not self == other
