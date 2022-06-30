import logging
import json

import numpy as np

from scipy.interpolate import splprep, splev
from pathlib import Path


class Test:
    def __init__(self, test_id, road_points: list[list], test_outcome, test_duration=None):
        """
        Class representing a test case.

        :param test_id: Unique test identifier
        :param road_points: Road points defining the test
        :param test_outcome: Outcome of the test execution
        :param test_duration: The duration of the test execution
        """
        self.test_id = test_id
        self.test_outcome = test_outcome
        self.predicted_test_outcome = None
        self.test_duration = test_duration
        self.road_points = road_points
        self.interpolated_road_points = self.__interpolate(road_points)
        self.simulation_data = []

    def save_as_json(self, file_path: Path):
        """

        :param file_path: File path to save the test as a json file
        """
        logging.info("save_as_json")
        with open(file_path, "w") as fp:
            test_dict = vars(self)
            json.dump(test_dict, fp, indent=2)

    @staticmethod
    def __interpolate(road_points: list[list]):
        """

        :param road_points:
        :return:
        """
        logging.info("* __interpolate")
        road_matrix = np.array(road_points)
        x = road_matrix[:, 0]
        y = road_matrix[:, 1]
        num_nodes = 50

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


if __name__ == "__main__":
    logging.info("* test.py")
