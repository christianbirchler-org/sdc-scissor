from math import sqrt

from self_driving.bbox import RoadBoundingBox
import numpy as np

# from code_pipeline.tests_generation import RoadTest
from code_pipeline.tests_generation import RoadTestFactory


def find_circle(p1, p2, p3):
    """
    Returns the center and radius of the circle passing the given 3 points.
    In case the 3 points form a line, returns (None, infinity).
    """
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])

    if abs(det) < 1.0e-6:
        return np.inf

    # Center of circle
    cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det

    radius = np.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
    return radius


def min_radius(x, w=5):
    mr = np.inf
    nodes = x
    for i in range(len(nodes) - w):
        p1 = nodes[i]
        p2 = nodes[i + int((w-1)/2)]
        p3 = nodes[i + (w-1)]
        radius = find_circle(p1, p2, p3)
        if radius < mr:
            mr = radius
    if mr == np.inf:
        mr = 0

    return mr * 3.280839895#, mincurv

class TestValidator:

    def __init__(self, map_size, min_road_length = 20):
        self.map_size = map_size
        self.box = (0, 0, map_size, map_size)
        self.road_bbox = RoadBoundingBox(self.box)
        self.min_road_length = min_road_length
        # Not sure how to set this value... This might require to compute some sort of density: not points that are too
        # close to each others
        self.max_points = 500

    def is_enough_road_points(self, the_test):
        return len(the_test.road_points) > 1

    def is_too_many_points(self, the_test):
        return len(the_test.road_points) > self.max_points

    def is_not_self_intersecting(self, the_test):
        road_polygon = the_test.get_road_polygon()
        return road_polygon.is_valid()

    def is_too_sharp(self, the_test, TSHD_RADIUS=47):
        if TSHD_RADIUS > min_radius(the_test.interpolated_points) > 0.0:
            check = True
        else:
            check = False
        return check

    def is_inside_map(self, the_test):
        """
            Take the extreme points and ensure that their distance is smaller than the map side
        """
        xs = [t[0] for t in the_test.interpolated_points]
        ys = [t[1] for t in the_test.interpolated_points]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        return 0 < min_x or min_x > self.map_size and \
               0 < max_x or max_x > self.map_size and \
               0 < min_y or min_y > self.map_size and \
               0 < max_y or max_y > self.map_size

    def is_right_type(self, the_test):
        """
            The type of the_test must be RoadTest
        """
        check = type(the_test) is RoadTestFactory.RoadTest
        return check

    def is_valid_polygon(self, the_test):
        road_polygon = the_test.get_road_polygon()
        check = road_polygon.is_valid()
        return check

    def intersects_boundary(self, the_test):
        road_polygon = the_test.get_road_polygon()
        check = self.road_bbox.intersects_boundary(road_polygon.polygon)
        return check

    def is_minimum_length(self, the_test):
        # This is approximated because at this point the_test is not yet interpolated
        return the_test.get_road_length() > self.min_road_length

    def validate_test(self, the_test):

        is_valid = True
        validation_msg = ""

        if not self.is_right_type(the_test):
            is_valid = False
            validation_msg = "Wrong type"
            return is_valid, validation_msg

        if not self.is_enough_road_points(the_test):
            is_valid = False
            validation_msg = "Not enough road points."
            return is_valid, validation_msg

        if self.is_too_many_points(the_test):
            is_valid = False
            validation_msg = "The road definition contains too many points"
            return is_valid, validation_msg

        if not self.is_inside_map(the_test):
            is_valid = False
            validation_msg = "Not entirely inside the map boundaries"
            return is_valid, validation_msg

        if self.intersects_boundary(the_test):
            is_valid = False
            validation_msg = "Not entirely inside the map boundaries"
            return is_valid, validation_msg

        if not self.is_valid_polygon(the_test):
            is_valid = False
            validation_msg = "The road is self-intersecting"
            return is_valid, validation_msg

        if not self.is_minimum_length(the_test):
            is_valid = False
            validation_msg = "The road is not long enough."
            return is_valid, validation_msg

        if self.is_too_sharp(the_test):
            is_valid = False
            validation_msg = "The road is too sharp"
            return is_valid, validation_msg

        return is_valid, validation_msg