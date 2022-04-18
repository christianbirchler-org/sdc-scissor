import logging
import time

from scipy.spatial import distance
from shapely.geometry import LineString, box

from sdc_scissor.testing_api.test import Test
from sdc_scissor.simulator_api.abstract_simulator import AbstractSimulator


class _RoadModel:
    def __init__(self, road_points: list[list]):
        self.coordinates = [(x[0], x[1]) for x in road_points]
        self.center_line: LineString = LineString(coordinates=self.coordinates)
        self.right_lane = self.center_line.buffer(distance=-5, single_sided=True)


class TestMonitor:
    def __init__(self, simulator: AbstractSimulator, test: Test):
        self.simulator = simulator
        self.test = test
        self.is_test_finished = False
        self.is_car_out_of_lane = False
        self.road = None
        self.start_time = None
        self.end_time = None
        self.data = []
        self.road_model = _RoadModel(test.interpolated_road_points)

    def check(self):
        logging.info('check')
        self.simulator.update_car()
        x_pos, y_pos, z_pos = self.simulator.get_car_position()
        current_time = time.time() - self.start_time
        logging.info('time: {}\tx: {}\ty: {}\tz: {}'.format(current_time, x_pos, y_pos, z_pos))
        self.data.append((current_time, x_pos, y_pos, z_pos))

        if self.__is_car_at_end_of_road(x_pos, y_pos) or self.__is_car_out_of_lane(x_pos, y_pos):
            self.is_test_finished = True
            self.end_time = time.time()
            self.test.test_duration = self.end_time - self.start_time
            self.test.simulation_data = self.data

    def start_timer(self):
        logging.info('start_timer')
        self.start_time = time.time()

    def stop_timer(self):
        logging.info('stop_timer')
        self.end_time = time.time()

    def dump_data(self):
        logging.info('dump_data')
        # TODO

    def __is_car_out_of_lane(self, x_pos: float, y_pos: float) -> bool:
        # TODO: Issue #22
        logging.info('__is_car_out_of_lane')
        car_model = box(x_pos-1, y_pos-1, x_pos+1, y_pos+1)
        is_car_model_inside_road_model = self.road_model.right_lane.covers(car_model)
        if not is_car_model_inside_road_model:
            logging.warning('CAR IS OFF THE LANE!')
        return not is_car_model_inside_road_model

    def __is_car_at_end_of_road(self, x_pos: float, y_pos: float) -> bool:
        logging.info('__car_at_end_of_road')
        road_end_point = self.test.interpolated_road_points[-1]
        x_end, y_end = road_end_point[0], road_end_point[1]
        res: bool = self.__are_points_close((x_pos, y_pos), (x_end, y_end), 8)
        return res

    @staticmethod
    def __are_points_close(a: tuple[float, float], b: tuple[float, float], threshold: float):
        dist = distance.euclidean(a, b)
        return dist < threshold


if __name__ == '__main__':
    logging.info('test_monitor.py')
