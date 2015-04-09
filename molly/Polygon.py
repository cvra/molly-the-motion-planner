"convex polygon with circular corners"


class Polygon(object):
    "convex polygon with circular corners"

    def __init__(self, corners, sides):
        # TODO verify input
        self.corners = corners
        self.sides = sides

    def tangent_circle(self, circle):
        "tangents between self and circle"
        all_tans = []

        for corner in self.corners:
            all_tans += circle.tangent_circle(corner)

        filter_side_intersections = [tan for tan in all_tans
                                     if all(not tan.intersect(side)
                                            for side in self.sides)]
        res = [tan for tan in filter_side_intersections
               if all(not tan.intersect_circle(corner)
                      for corner in self.corners)]

        return res

    def intersects_tangent(self, tangent):
        "return whether tangent intersects self"

        for circle in self.corners:
            if circle.intersects_tangent(tangent):
                return True

        for side in self.sides:
            if side.intersect(tangent):
                return True

        return False

    def tangent_polygon(self, poly):
        "return tangents between self and other polygon"

        possible_tans = []

        for corner in self.corners:
            possible_tans += poly.tangent_circle(corner)

        side_intersections = [tan for tan in possible_tans
                              if all(not tan.intersect(side)
                                     for side in self.sides)]
        res = [tan for tan in side_intersections
               if all(not tan.intersect_circle(corner)
                      for corner in self.corners)]

        return res

    def __add__(self, vec):
        "translate polygon by vec"
        new_corners = [corner + vec for corner in self.corners]
        new_sides = [side + vec for side in self.sides]

        return Polygon(new_corners, new_sides)

    def __eq__(self, other):

        if len(self.corners) != len(other.corners):
            return False

        equal_corners = all(c1 == c2
                            for c1, c2 in zip(self.corners, other.corners))
        equal_sides = all(s1 == s2
                          for s1, s2 in zip(self.sides, other.sides))

        return equal_corners and equal_sides

    def __ne__(self, other):
        return not self == other
