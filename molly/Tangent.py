"tangent class"

from molly.Vec2D import Vec2D

class Tangent(object):
    "tangent class"

    def __init__(self,
                 start_pos,
                 start_circle,
                 start_orientation,
                 end_pos,
                 end_circle,
                 end_orientation):

        self.start_pos = start_pos
        self.start_circle = start_circle
        self.start_orient = start_orientation
        self.end_pos = end_pos
        self.end_circle = end_circle
        self.end_orient = end_orientation

    def intersect(self, other):
        "return whether self and other tangent intersect \
        https://stackoverflow.com/questions/563198/ \
        how-do-you-detect-where-two-line-segments-intersect"

        dir1 = self.end_pos - self.start_pos
        dir2 = other.end_pos - other.start_pos

        dir_cross_prod = dir1.cross(dir2)
        diff = (other.start_pos - self.start_pos)
        diff_cross_dir1 = diff.cross(dir1)

        if abs(dir_cross_prod) < Vec2D.EPSILON and \
           abs(diff_cross_dir1) < Vec2D.EPSILON:

            cond1 = 0 <= diff.dot(dir1) <= dir1.dot(dir1)
            cond2 = 0 <= (-diff).dot(dir2) <= dir2.dot(dir2)
            return cond1 or cond2
        elif abs(dir_cross_prod) < Vec2D.EPSILON:
            return False
        else:
            param_u = diff_cross_dir1 / dir_cross_prod
            param_t = diff.cross(dir2) / dir_cross_prod
            return 0 <= param_u <= 1 and 0 <= param_t <= 1

    def intersect_circle(self, circle):
        "return whether self intersects circle"
        return circle.intersects_tangent(self)

    def __eq__(self, other):

        if self.start_pos == other.start_pos:
            same_start_circle = self.start_circle == other.start_circle
            same_end_circle = self.end_circle == other.end_circle
            same_end_pos = self.end_pos == other.end_pos
            same_start_orient = self.start_orient * other.start_orient > 0
            same_end_orient = self.end_orient * other.end_orient > 0

            return same_start_circle and \
                   same_end_circle and \
                   same_end_pos and \
                   same_start_orient and \
                   same_end_orient
        if self.start_pos == other.end_pos:
            same_start_circle = self.start_circle == other.end_circle
            same_end_circle = self.end_circle == other.start_circle
            same_end_pos = self.end_pos == other.start_pos
            same_start_orient = self.start_orient * other.end_orient > 0
            same_end_orient = self.end_orient * other.start_orient > 0

            return same_start_circle and \
                   same_end_circle and \
                   same_end_pos and \
                   same_start_orient and \
                   same_end_orient
        else:
            return False

    def __ne__(self, other):
        return not self == other
