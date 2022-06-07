import abc


class SegmentationStrategy(abc.ABC):
    """
    Interface for implementing different segmentation strategies.
    """

    @abc.abstractmethod
    def extract_segments(self, road_points):
        """
        Abstract method to retrieve segments from a road, based on a specific strategy.

        :param road_points: Sequence of coordinates specifying the road.
        """
        pass
