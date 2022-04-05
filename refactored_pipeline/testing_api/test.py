import logging
import numpy as np

from scipy.interpolate import CubicSpline, splprep, splev


class Test:
    def __init__(self, road_points: list[list]):
        self.road_points = road_points
        self.interpolated_points = self.__interpolate(road_points)

        # add z-coordinate and road width to the test
        for road_point in self.interpolated_points:
            road_point.extend([-28, 10])

    @staticmethod
    def __interpolate(road_points: list[list]):
        logging.info('* __interpolate')
        road_matrix = np.array(road_points)
        x = road_matrix[:, 0]
        y = road_matrix[:, 1]
        num_nodes = 8

        if len(x) == 2:
            # With two points the only option is a straight segment
            k = 1
        elif len(y) == 3:
            # With three points we use an arc, using linear interpolation will result in invalid road tests
            k = 2
        else:
            # Otheriwse, use cubic splines
            k = 3

        pos_tck, *_pos_u = splprep([x, y], s=0, k=k)
        step_size = 1 / num_nodes
        unew = np.arange(0, 1 + step_size, step_size)
        x_new, y_new = splev(unew, pos_tck)
        new_road_points = np.column_stack((x_new, y_new)).tolist()

        return new_road_points


if __name__ == '__main__':
    logging.info('* test.py')
