from .segmentation_strategy import SegmentationStrategy

class MaximumAngleStrategy(SegmentationStrategy):
    """
    Define segments based on identified turns. The center of a turn where the
    angles possibly reaches the maximum will also be the center of the segment.
    Straight segments are identified where no significant turn angles are present.
    """

    def __init__(self):
        self.__road_geometry_calculator = RoadGeometryCalculator()

    def extract_segments(self, road_points):
        pass
