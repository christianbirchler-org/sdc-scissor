import logging

from sdc_scissor.feature_extraction_api.segmentation_strategy import SegmentationStrategy
from sdc_scissor.feature_extraction_api.road_geometry_calculator import RoadGeometryCalculator


class AngleBasedStrategy(SegmentationStrategy):
    """
    Define segments based on identified turns. The center of a turn where the
    angles possibly reaches the maximum will also be the center of the segment.
    Straight segments are identified where no significant turn angles are present.
    """

    def __init__(self, angle_threshold=5, decision_distance=10):
        """
        Instantiate a strategy object defining the segmentation strategy of the road. Class is coherent to the strategy pattern.

        :param angle_threshold: Angle threshold defining a new segment.
        :param decision_distance: Road distance for calculating the turn angle.
        """
        self.__road_geometry_calculator = RoadGeometryCalculator()
        self.__angle_threshold = angle_threshold
        self.__decision_distance = decision_distance

    def extract_segments(self, road_points):
        """
        Extract segments from road points according to the angle-based segmentation strategy.

        :param road_points: List of 2D  points, defining the road to be segmented
        :return: List of indexes defining the start and end of segments
        """
        # iterate according to the decision distance
        segment_indexes = []
        segment_start_index = 0
        current_road_piece_start_index = 0
        current_angle = 0
        is_first_piece = True
        is_last_iteration = False

        for i in range(len(road_points)):
            # check if it is the last iteration
            if i == (len(road_points) - 1):
                is_last_iteration = True

            # the start of a new piece has to be 2 indexes ahead of the current i
            if current_road_piece_start_index == i + 1:
                current_road_piece_end_index = i + 2
            else:
                current_road_piece_end_index = i + 1

            # define the current road piece to calculate the turn angle and distance
            current_road_piece = road_points[current_road_piece_start_index : current_road_piece_end_index + 1]

            # calculate the road piece distance defined above
            current_distance = self.__road_geometry_calculator.get_road_length(current_road_piece)

            # check if the distance of the current road piece is long enough or it is the last iteration
            if (current_distance >= self.__decision_distance) or is_last_iteration:
                previous_angle = current_angle

                # calculate the angle of the current road piece
                # TODO: ensure that the road piece to calculate the angle has enough points!!!
                # (e.g., use temporarily a longer road piece)
                if len(current_road_piece) == 2 and current_road_piece_start_index > 0:
                    tmp_current_road_piece = road_points[
                        current_road_piece_start_index - 1 : current_road_piece_end_index + 1
                    ]
                else:
                    tmp_current_road_piece = current_road_piece
                current_angle = sum(self.__road_geometry_calculator.extract_turn_angles(tmp_current_road_piece))

                # define start and end index of segment iff the angle of the current road piece is different
                if (
                    self.__has_current_angle_changed(previous_angle, current_angle) and not is_first_piece
                ) or is_last_iteration:
                    segment_end_index = i
                    segment_indexes.append((segment_start_index, segment_end_index))
                    segment_start_index = segment_end_index + 1
                    current_road_piece_start_index = segment_start_index
                else:
                    current_road_piece_start_index = current_road_piece_end_index + 1
                    is_first_piece = False

        return segment_indexes

        # decide type of segment based on angle and its threshold
        # define segment when the type of segment will change

    def __has_current_angle_changed(self, previous_angle, current_angle):
        """
        Check if there is a significant change of turn angles.

        :param previous_angle: Previous angle
        :param current_angle: Current angle to be compared with the previous angle
        :return: True or False if there is a change greater than the specified threshold
        """
        angle_threshold = self.__angle_threshold
        if current_angle <= previous_angle + angle_threshold and current_angle >= previous_angle - angle_threshold:
            return False
        return True


if __name__ == "__main__":
    logging.info("angle_based_strategy.py")
