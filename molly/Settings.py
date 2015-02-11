"general settings class for molly"

from molly.Circle import Circle
from molly.Vec2D import Vec2D
from molly.Tangent import Tangent
from molly.Polygon import Polygon

CIRCLE1 = Circle(Vec2D(0, 0), 0.2)
CIRCLE2 = Circle(Vec2D(1.066, 0), 0.2)
CIRCLE3 = Circle(Vec2D(1.066, 0.6), 0.2)
CIRCLE4 = Circle(Vec2D(0, 0.6), 0.2)

CORNERS = [CIRCLE1, CIRCLE2, CIRCLE3, CIRCLE4]

SIDE1 = Tangent(Vec2D(0, -0.2), CIRCLE1, -1, Vec2D(1.066, -0.2), CIRCLE2, 1)
SIDE2 = Tangent(Vec2D(1.086, 0), CIRCLE2, -1, Vec2D(1.086, 0.6), CIRCLE3, 1)
SIDE3 = Tangent(Vec2D(1.066, 0.8), CIRCLE3, -1, Vec2D(0, 0.8), CIRCLE4, 1)
SIDE4 = Tangent(Vec2D(-0.2, 0.6), CIRCLE4, -1, Vec2D(-0.2, 0), CIRCLE1, 1)

SIDES = [SIDE1, SIDE2, SIDE3, SIDE4]

STAIRS = Polygon(CORNERS, SIDES)

class Settings(object):
    "settings class memorizing settings for molly"

    def __init__(self,
                 max_acc=1.6,
                 max_v=0.6,
                 time_resolution=0.1,
                 static_poly_obs=[],
                 static_circ_obs=[],
                 obs_min_r=0.1,
                 playground_dim=(3.0, 2.0)):

        self.max_acc = max_acc
        self.max_v = max_v
        self.obs_min_r = obs_min_r
        (self.width, self.height) = playground_dim
        self.static_poly_obs = static_poly_obs
        self.static_circ_obs = static_circ_obs
        self.time_resolution = time_resolution
        corner1 = Vec2D(0, 0)
        corner2 = Vec2D(self.width, 0)
        corner3 = Vec2D(self.width, self.height)
        corner4 = Vec2D(0, self.height)
        border1 = Tangent(corner1, None, 0, corner2, None, 0)
        border2 = Tangent(corner2, None, 0, corner3, None, 0)
        border3 = Tangent(corner3, None, 0, corner4, None, 0)
        border4 = Tangent(corner4, None, 0, corner1, None, 0)
        self.bounds = [border1, border2, border3, border4]

