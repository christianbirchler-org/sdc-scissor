class Test:
    def __init__(self, road_points: list[tuple]):
        self.road_points = road_points
        self.interpolated_points = self.__interpolate(road_points)

    @staticmethod
    def __interpolate(road_points: list[tuple]):
        return road_points


if __name__ == '__main__':
    print('* test.py')
