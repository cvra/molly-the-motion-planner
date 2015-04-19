"convex polygon with circular corners"


class Polygon(object):
    "convex polygon with circular corners"

    def __init__(self, corners, sides=None):
        if sides is not None:
            self.corners = corners
            self.sides = sides
        elif len(corners) < 2:
            raise ValueError("trying to initialize polygon from single circle")
        else:
            circle1 = corners[0]
            circle2 = corners[1]
            (cor, sid) = _from_circle_collection(circle1, circle2, corners[2:])

            self.corners = cor
            self.sides = sid

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

    def circumference(self):
        "circumference of this polygon"
        acc = 0
        circle_dict = {}

        for tan in self.sides:
            acc += (tan.start_pos - tan.end_pos).length()

            if circle_dict.get(tan.start_circle) is None:
                circle_dict[tan.start_circle] = []

            circle_dict[tan.start_circle].append((tan.start_pos, tan.start_orient))

            if circle_dict.get(tan.end_circle) is None:
                circle_dict[tan.end_circle] = []

            circle_dict[tan.end_circle].append((tan.end_pos, tan.end_orient))

        for circ in circle_dict:
            points = circle_dict[circ]
            (start, sori) = points[0]
            (end, _) = points[1]

            acc += dist_on_circle(start, end, circ, sori)

        return acc

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


def dist_on_circle(start, end, circle, orientation):
    "distance between start and end on circle (orientation from end)"
    vec1 = (start - circle.pos).normalized()
    vec2 = (end - circle.pos).normalized()

    if orientation > 0:
        angle = vec1.oriented_angle(vec2)
    else:
        angle = vec2.oriented_angle(vec1)

    return angle * circle.radius

def _from_circle_collection(circle1, circle2, circles):
    "computes sides and corners of a polygon from an arbitrary \
    collection of circles"

    tans = circle1._outertangents(circle2)
    visited = set([circle1, circle2])

    for new_circle in circles:
        for old_circle in visited:
            tans += new_circle._outertangents(old_circle)

        visited.add(new_circle)

    to_remove = set()

    for tan1 in tans:
        for tan2 in tans:
            if tan1.intersect(tan2) and not tan1 == tan2:
                to_remove.add(tan1)
                to_remove.add(tan2)

    filtered = set()

    for tan in tans:
        if not tan in to_remove:
            filtered.add(tan)

    corners = set()

    for tan in filtered:
        corners.add(tan.start_circle)
        corners.add(tan.end_circle)

    return (list(corners), list(filtered))

