import numpy as np

from self_driving.bbox import RoadBoundingBox

# from code_pipeline.tests_generation import RoadTest
# from code_pipeline.tests_generation import RoadTestFactory
from sdc_scissor.feature_extraction_api.road_geometry_calculator import RoadGeometryCalculator


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
    cx = (bc * (p2[1] - p3[1]) - cd * (p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det

    radius = np.sqrt((cx - p1[0]) ** 2 + (cy - p1[1]) ** 2)
    return radius


def min_radius(x, w=5):
    mr = np.inf
    nodes = x
    for i in range(len(nodes) - w):
        p1 = nodes[i]
        p2 = nodes[i + int((w - 1) / 2)]
        p3 = nodes[i + (w - 1)]
        radius = find_circle(p1, p2, p3)
        if radius < mr:
            mr = radius
    if mr == np.inf:
        mr = 0

    return mr * 3.280839895  # , mincurv


class TestValidator:
    def __init__(self, map_size, min_road_length=20):
        self.road_geometry_calculator = RoadGeometryCalculator()
        self.map_size = map_size
        self.box = (0, 0, map_size, map_size)
        self.road_bbox = RoadBoundingBox(self.box)
        self.min_road_length = min_road_length
        # Not sure how to set this value... This might require to compute some sort of density: not points that are too
        # close to each others
        self.max_points = 500

    @staticmethod
    def is_enough_road_points(the_test):
        return len(the_test.road_points) > 1

    def is_too_many_points(self, the_test):
        return len(the_test.road_points) > self.max_points

    @staticmethod
    def is_not_self_intersecting(the_test):
        road_polygon = the_test.get_road_polygon()
        return road_polygon.is_valid()

    @staticmethod
    def is_too_sharp(the_test, TSHD_RADIUS=47):
        return TSHD_RADIUS > min_radius(the_test.interpolated_road_points) > 0.0

    def is_inside_map(self, the_test):
        """
        Take the extreme points and ensure that their distance is smaller than the map side
        """
        xs = [t[0] for t in the_test.interpolated_road_points]
        ys = [t[1] for t in the_test.interpolated_road_points]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        return (
            min_x > 0
            or min_x > self.map_size
            and max_x > 0
            or max_x > self.map_size
            and min_y > 0
            or min_y > self.map_size
            and max_y > 0
            or max_y > self.map_size
        )

    @staticmethod
    def is_right_type(the_test):
        """
        The type of the_test must be RoadTest
        """
        # check = isinstance(the_test, RoadTestFactory.RoadTest)
        # return check

    @staticmethod
    def is_valid_polygon(the_test):
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

    @staticmethod
    def is_min_road_segment_not_long_enough_according_risk_factor(the_test):
        rf = the_test.risk_factor
        msl = the_test.min_segment_length
        required_min_segment_length = None
        if rf == 1:
            required_min_segment_length = 50
        elif rf == 1.5:
            required_min_segment_length = 30
        elif rf == 2:
            required_min_segment_length = 20
        else:
            raise Exception("Min seg length for RF {} not defined".format(rf))

        return msl >= required_min_segment_length

    def is_road_not_long_enough_according_min_segment(self, the_test):
        required_proportion = 0.4  # TODO: avoid magic number
        road_length = self.road_geometry_calculator.get_road_length(the_test.road_points)
        msl = the_test.min_segment_length
        return road_length * required_proportion >= msl

    def validate_test(self, the_test):

        is_valid = True
        validation_msg = ""

        # if not self.is_right_type(the_test):
        #     is_valid = False
        #     validation_msg = "Wrong type"
        #     return is_valid, validation_msg

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

        # if self.intersects_boundary(the_test):
        #     is_valid = False
        #     validation_msg = "Not entirely inside the map boundaries"
        #     return is_valid, validation_msg
        #
        # if not self.is_valid_polygon(the_test):
        #     is_valid = False
        #     validation_msg = "The road is self-intersecting"
        #     return is_valid, validation_msg
        #
        # if not self.is_minimum_length(the_test):
        #     is_valid = False
        #     validation_msg = "The road is not long enough."
        #     return is_valid, validation_msg
        #
        # if self.is_too_sharp(the_test):
        #     is_valid = False
        #     validation_msg = "The road is too sharp"
        #     return is_valid, validation_msg

        # if self.is_min_road_segment_not_long_enough_according_risk_factor(the_test):
        #     is_valid = False
        #     validation_msg = "Min road segment is too short for the risk factor"
        #     return is_valid, validation_msg

        # if self.is_road_not_long_enough_according_min_segment(the_test):
        #     is_valid = False
        #     validation_msg = "Road is too short according the min segment"
        #     return is_valid, validation_msg

        return is_valid, validation_msg
