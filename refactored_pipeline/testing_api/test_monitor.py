import logging
import time

from scipy.spatial import distance

from refactored_pipeline.testing_api.test import Test
from refactored_pipeline.simulator_api.abstract_simulator import AbstractSimulator


class TestMonitor:
    def __init__(self, simulator: AbstractSimulator, vehicle: Vehicle, test: Test):
        self.simulator = simulator
        self.vehicle = vehicle
        self.test = test
        self.is_car_at_end_of_road = False
        self.car_is_out_of_lane = False
        self.road = None
        self.start_time = None
        self.end_time = None
        self.data = {}

    def check(self):
        logging.info('* check')
        self.simulator.update_sensors()
        self.vehicle.update_vehicle()
        # TODO: implement 'update_sensors' from the abstract base class of the simulator
        sensors = self.simulator.poll_sensors(self.vehicle)
        state = self.vehicle.state
        x_pos = state['pos'][0]
        y_pos = state['pos'][1]
        logging.info('** x: {}\ny: {}\n\n'.format(x_pos, y_pos))
        if self.__car_at_end_of_road(x_pos, y_pos):
            self.is_car_at_end_of_road = True

    def start_timer(self):
        logging.info('start_timer')
        self.start_time = time.time()

    def stop_timer(self):
        logging.info('stop_timer')
        self.end_time = time.time()

    def dump_data(self):
        logging.info('dump_data')
        # TODO

    def __is_car_at_end_of_road(self, x_pos: float, y_pos: float) -> bool:
        logging.info('__car_at_end_of_road')
        road_end_point = self.test.interpolated_points[-1]
        x_end, y_end = road_end_point[0], road_end_point[1]
        res: bool = self.__are_points_close((x_pos, y_pos), (x_end, y_end), 8)
        return res

    @staticmethod
    def __are_points_close(a: tuple[float, float], b: tuple[float, float], threshold: float):
        dist = distance.euclidean(a, b)
        return dist < threshold


if __name__ == '__main__':
    logging.info('test_monitor.py')
