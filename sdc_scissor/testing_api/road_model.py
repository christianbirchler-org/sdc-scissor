from shapely.geometry import LineString


class RoadModel:
    def __init__(self, road_points: list[list]):
        self.coordinates = [(x[0], x[1]) for x in road_points]
        self.center_line: LineString = LineString(coordinates=self.coordinates)
        self.right_lane = self.center_line.buffer(distance=-5, single_sided=True)
        self.ideal_trajectory: LineString = self.center_line.parallel_offset(distance=2.5)
