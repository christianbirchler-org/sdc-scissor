from feature_extraction.segmentation_strategies.segmentation_strategy import SegmentationStrategy

class EquiDistanceStrategy(SegmentationStrategy):
    """
    Define segments with equal lengts. The last segment might be different to
    the others since there might be a remainder while dividing the road into
    predefined number of segments.
    """
    def __init__(self, number_of_segments):
        super().__init__()
        self.__number_of_segments = number_of_segments

    def extract_segments(self, road_points):
        segments = []

        # only two road points for a segment
        max_number_of_possible_segments = len(road_points) - 1

        number_of_road_points = len(road_points)

        if number_of_road_points < self.__number_of_segments:
            raise Exception("Not enough road points.")

        # TODO: Verify if this calculation is correct. I am not sure!
        road_points_per_segment = 1 + round(max_number_of_possible_segments/self.__number_of_segments)

        # calculate for each segments its start/end road point indeces
        end = 0
        for i in range(self.__number_of_segments):
            start = end

            # check if last segment because last segment might have more/less points
            if i == self.__number_of_segments-1:
                end = len(road_points) - 1
            else:
                end = start + road_points_per_segment - 1
            
            current_segment = (start, end)
            segments.append(current_segment)

        return segments

