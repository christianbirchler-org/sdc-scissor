import math
import time
import logging
from math import sqrt

from beamngpy import BeamNGpy, Scenario, Vehicle, Road, BNGError
from beamngpy.sensors import Electrics

from refactored_pipeline.testing_api.test_loader import TestLoader
from refactored_pipeline.testing_api.test import Test
from refactored_pipeline.testing_api.test_loader import TestLoader
from refactored_pipeline.testing_api.test_monitor import TestMonitor


class TestRunner:
    def __init__(self, **kwargs) -> None:
        self.test_loader: TestLoader = kwargs.get('test_loader', None)
        self.ml_component = kwargs.get('machine_learning_api', None)
        self.simulator: BeamNGpy = kwargs.get('simulator', None)
        self.vehicle = None

    def run_test_suite(self):
        logging.info('* run_test_suite')

        while self.test_loader.has_next():
            test: Test = self.test_loader.next()
            self.run(test)

    def load_test(self, test: Test):
        logging.info('* load_test')
        self.test_loader.load(test)

    def setup_scenario(self):
        logging.info('* setup_scenario')
        scenario = Scenario('tig', 'example')
        road = Road(material='tig_road_rubber_sticky', rid='flat_road', interpolate=True)
        road.nodes.extend(self.test_loader.current_test.interpolated_points)

        scenario.add_road(road)

        self.vehicle = Vehicle(vid='ego_vehicle', model='etk800', licence='Scissor')
        electrics = Electrics()
        self.vehicle.attach_sensor('electrics', electrics)

        x_start, y_start, z_start, x_dir, y_dir, alpha = self.__compute_start_position(self.test_loader.current_test)
        rot_quat = (0, 0, 1, -0.1)
        rot = (0, 0, alpha / (2 * math.pi))
        scenario.add_vehicle(self.vehicle, pos=(x_start, y_start, z_start), rot_quat=rot_quat)

        end_point = self.test_loader.current_test.interpolated_points[-1][:3]

        scenario.add_checkpoints(positions=[end_point], scales=[(5, 5, 5)], ids=['end_point'])
        scenario.make(self.simulator)

        self.simulator.load_scenario(scenario)

    def run(self, test: Test) -> None:
        """
        Runs the test with the simulator given by instantiation of the test runner.
        """
        logging.info('* run')

        scenario.add_checkpoints(positions=[end_point], scales=[(5, 5, 5)], ids=['end_point'])
        scenario.make(self.simulator)

        self.simulator.load_scenario(scenario)
        self.simulator.start_scenario()

        vehicle.ai_set_mode('span')
        vehicle.ai_drive_in_lane(lane=True)
        vehicle.ai_set_aggression(0.5)
        vehicle.set_color(rgba=(0, 0, 1, 0.5))
        vehicle.ai_set_speed(12)
        vehicle.ai_set_waypoint('end_point')
        # vehicle.start_in_game_logging(outputDir='./')

        test_monitor = TestMonitor(self.simulator, vehicle, test)
        while not test_monitor.is_car_at_end_of_road:
            # try:
            #     print('waypoints: {}'.format(scenario.find_waypoints()))
            # except BNGError:
            #     pass
            try:
                test_monitor.check()
            except Exception:
                logging.info('* run except clause')
                time.sleep(10)
                # self.simulator.connect()
                self.simulator.start_scenario()
            time.sleep(0.1)

        input('Hit enter...')

    @staticmethod
    def __compute_start_position(test: Test):
        logging.info('* compute_start_position')
        first_road_point = test.interpolated_points[0]
        second_road_point = test.interpolated_points[1]
        x_dir, y_dir = (second_road_point[0] - first_road_point[1], second_road_point[1] - first_road_point[1])
        x_dir_norm, y_dir_norm = (x_dir / sqrt(x_dir ** 2 + y_dir ** 2), y_dir / sqrt(x_dir ** 2 + y_dir ** 2))
        alpha = math.asin(y_dir_norm)

        x_cross_dir_norm, y_cross_dir_norm = y_dir_norm, -x_dir_norm

        return first_road_point[0] + 2.5 * x_cross_dir_norm, first_road_point[1] + 2.5 * y_cross_dir_norm, -28.0, x_dir, y_dir, alpha


if __name__ == '__main__':
    logging.info('* test_runner.py')
