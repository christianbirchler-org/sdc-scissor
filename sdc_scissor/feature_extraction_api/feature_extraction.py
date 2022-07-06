import logging
import math
import statistics

import pandas as pd
import numpy as np

from pathlib import Path
from shapely.geometry import Point, LineString

from sdc_scissor.feature_extraction_api.road_geometry_calculator import RoadGeometryCalculator
from sdc_scissor.testing_api.test import Test


class RoadFeatures:
    def __init__(self):
        """
        Class representing the road features as attributes
        """
        self.direct_distance = 0
        self.road_distance = 0
        self.num_l_turns = 0
        self.num_r_turns = 0
        self.num_straights = 0
        self.median_angle = 0
        self.total_angle = 0
        self.mean_angle = 0
        self.std_angle = 0
        self.max_angle = 0
        self.min_angle = 0
        self.median_pivot_off = 0
        self.mean_pivot_off = 0
        self.std_pivot_off = 0
        self.max_pivot_off = 0
        self.min_pivot_off = 0
        self.start_time = 0
        self.end_time = 0
        self.test_duration = 0
        self.mean_road_diversity = 0
        self.full_road_diversity = 0
        self.safety = None

    def to_dict(self):
        """
        Serialize the road features to a python dictionary

        :return: A dictionary with the road features
        """
        members = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        res = {}
        for member in members:
            res[member] = [getattr(self, member)]
        return res


class RoadSegment:
    def __init__(self):
        """
        A class representing a road segment
        """
        self.start_index = None
        self.end_index = None
        self.type = None
        self.angle = None
        self.radius = None
        self.segment_mean_diversity = None
        self.segment_total_diversity = None


class SegmentType:
    l_turn = "left_turn"
    r_turn = "right_turn"
    straight = "straight"


class FeatureExtractor:
    def __init__(self, segmentation_strategy):
        """
        A class that is responsible for extracting road features of test scenarios.

        :param segmentation_strategy: A road segmentation strategy
        """
        self.__road_features = RoadFeatures()
        self.__segments = []
        self.__road_geometry_calculator = RoadGeometryCalculator()
        self.__segmentation_strategy = segmentation_strategy

    @staticmethod
    def save_to_csv(road_features: list, out_dir: Path):
        """
        Save the road features to a csv file.

        :param road_features: List of road features
        :param out_dir: Path to store the csv file
        """
        logging.info("save_to_csv")
        dd = pd.DataFrame()
        for test_id, rf, duration in road_features:
            rf_dict = rf.to_dict()
            rf_dict["test_id"] = test_id
            rf_dict["duration"] = duration
            logging.info(rf_dict)
            rf_dd = pd.DataFrame(rf_dict)
            logging.info(rf_dd)
            dd = pd.concat([dd, rf_dd], ignore_index=True)

        logging.info(dd)
        out_path = out_dir / "road_features.csv"
        dd.to_csv(out_path)

    def extract_features(self, test: Test) -> RoadFeatures:
        """
        Input is a list of (x, y) tuples which defines the road.
        This function extract the angles and radius of segments.
        Furthermore, the statistics of angles and radius are calculated.

        :param test: A test object
        :return: A road feature object
        """
        segment_indexes_list = self.__segmentation_strategy.extract_segments(test.road_points)
        for indexes in segment_indexes_list:
            segment: RoadSegment = self.__get_road_segment_with_features(test, indexes)
            self.__segments.append(segment)

        self.__road_features = self.__get_full_road_features_from(test, self.__segments)
        return self.__road_features

    def __get_full_road_features_from(self, test: Test, segments: list[RoadSegment]):
        """
        Compute full road features based on all segments.

        :param test: Test object.
        :param segments: List of road segments.
        :return: An object containing road features as attributes.
        """
        road_features = RoadFeatures()
        road_features.test_duration = test.test_duration

        raw_feature_data = {"angles": [], "pivots": [], "diversities": []}

        for segment in segments:
            if segment.type == SegmentType.l_turn:
                road_features.num_l_turns += 1
            elif segment.type == SegmentType.r_turn:
                road_features.num_r_turns += 1
            elif segment.type == SegmentType.straight:
                road_features.num_straights += 1
            road_features.total_angle += segment.angle

            # these lists allows a simpler calculation of the statistics
            raw_feature_data["angles"].append(segment.angle)
            raw_feature_data["pivots"].append(segment.radius)
            raw_feature_data["diversities"].append(segment.segment_mean_diversity)

        road_features.mean_road_diversity = float(np.mean(raw_feature_data["diversities"]))
        road_features.full_road_diversity = float(np.sum(raw_feature_data["diversities"]))

        road_features.mean_angle = statistics.mean(raw_feature_data["angles"])
        road_features.median_angle = statistics.median(raw_feature_data["angles"])
        road_features.max_angle = max(raw_feature_data["angles"])
        road_features.min_angle = min(raw_feature_data["angles"])

        # more than 1 data point is required to calculate the standard deviation
        if len(raw_feature_data["angles"]) > 1:
            road_features.std_angle = statistics.stdev(raw_feature_data["angles"])
        else:
            road_features.std_angle = 0

        road_features.mean_pivot_off = statistics.mean(raw_feature_data["pivots"])
        road_features.median_pivot_off = statistics.median(raw_feature_data["pivots"])
        road_features.max_pivot_off = max(raw_feature_data["pivots"])
        road_features.min_pivot_off = min(raw_feature_data["pivots"])

        if len(raw_feature_data["pivots"]) > 1:
            road_features.std_pivot_off = statistics.stdev(raw_feature_data["pivots"])
        else:
            road_features.std_pivot_off = 0

        road_features.direct_distance = self.__road_geometry_calculator.get_distance_between(
            test.road_points[0], test.road_points[-1]
        )
        road_features.road_distance = self.__road_geometry_calculator.get_road_length(test.road_points)

        return road_features

    def __get_segment_type(self, test: Test, road_segment, angle_threshold):
        """
        Return the type of segment (straight, left turn, right turn). The segment
        is defined by its start and end index that are already specified.
        :param test:
        :param road_segment:
        :param angle_threshold:
        :return:
        """
        start_index = road_segment.start_index
        end_index = road_segment.end_index

        segment_road_points = test.road_points[start_index : end_index + 1]

        angles_lst = self.__road_geometry_calculator.extract_turn_angles(segment_road_points)

        angles_sum = sum(angles_lst)

        if angle_threshold > angles_sum > -angle_threshold:
            return SegmentType.straight
        if angles_sum >= angle_threshold:
            return SegmentType.l_turn
        if angles_sum <= angle_threshold:
            return SegmentType.r_turn

    def __get_segment_angle(self, test: Test, road_segment):
        """

        :param test:
        :param road_segment:
        :return:
        """
        start_index = road_segment.start_index
        end_index = road_segment.end_index

        segment_road_points = test.road_points[start_index : end_index + 1]

        angles_lst = self.__road_geometry_calculator.extract_turn_angles(segment_road_points)

        angles_sum = sum(angles_lst)

        return angles_sum

    def __get_segment_radius(self, test: Test, road_segment):
        """

        :param test:
        :param road_segment:
        :return:
        """
        if road_segment.type == SegmentType.straight:
            return 0

        start_index = road_segment.start_index
        end_index = road_segment.end_index

        segment_road_points = test.road_points[start_index : end_index + 1]

        angles_lst = self.__road_geometry_calculator.extract_turn_angles(segment_road_points)
        segment_length = self.__road_geometry_calculator.get_road_length(segment_road_points)

        angles_sum = sum(angles_lst)

        unsigned_angle = abs(angles_sum)

        # C=2*pi*r
        proportion = unsigned_angle / 360
        circle_length = segment_length / proportion
        radius = circle_length / (2 * math.pi)

        return radius

    def __get_segment_diversity(self, test: Test, road_segment: RoadSegment) -> tuple:
        """
        Compute the diversity of the road segment compared to a straight trajectory.

        :param test: A test object
        :param road_segment: A road segment object
        :return: The measure of diversity
        """
        road_points = test.road_points
        start_index, end_index = road_segment.start_index, road_segment.end_index
        segment_road_points = road_points[start_index : end_index + 1]
        start_point, end_point = Point(segment_road_points[0][:2]), Point(segment_road_points[-1][:2])
        direct_segment_line: LineString = LineString([start_point, end_point])

        shapely_points: list = [Point(rp[0], rp[1]) for rp in segment_road_points]
        segment_line: LineString = LineString(shapely_points)

        point_to_line_distances = [direct_segment_line.distance(point) for point in shapely_points]
        segment_total_diversity = float(np.sum(point_to_line_distances))
        segment_mean_diversity = float(np.mean(point_to_line_distances))
        return segment_total_diversity, segment_mean_diversity

    def __get_road_segment_with_features(self, test: Test, indexes) -> RoadSegment:
        """
        Compute segment features and create a segment object accordingly.

        :param test: A test object
        :param indexes: Start and end index of a single segment of the road specified in the test.
        :return: A road segment object with segment specific features.
        """
        road_segment = RoadSegment()
        road_segment.start_index = indexes[0]
        road_segment.end_index = indexes[1]

        # classify segment type
        road_segment.type = self.__get_segment_type(test, road_segment, angle_threshold=5)

        # update angle
        road_segment.angle = self.__get_segment_angle(test, road_segment)

        # calculate radius
        road_segment.radius = self.__get_segment_radius(test, road_segment)

        road_segment.segment_total_diversity, road_segment.segment_mean_diversity = self.__get_segment_diversity(
            test, road_segment
        )

        return road_segment
