import logging
import math
import time

from beamngpy import BeamNGpy, Scenario, Road, Vehicle
from beamngpy.sensors import Electrics

from sdc_scissor.simulator_api.abstract_simulator import AbstractSimulator
from sdc_scissor.testing_api.test import Test


class BeamNGSimulator(AbstractSimulator):
    def __init__(self, host: str, port: int, home: str, user: str):
        super().__init__()
        self.host = host
        self.port = port
        self.home = home
        self.user = user
        self.beamng = BeamNGpy(host, port, home=home, user=user)
        self.vehicle = None
        self.car_state = None
        self.scenario = None

    def open(self):
        self.beamng.open()

    def close(self):
        self.beamng.close()

    def create_new_instance(self):
        logging.info('restart simulator')
        try:
            self.beamng.close()
        finally:
            logging.info('creating a new BeamNGpy instance')
            time.sleep(5)
            self.beamng = BeamNGpy(self.host, self.port, home=self.home, user=self.user)

    def stop_scenario(self):
        logging.info('stop_scenario')
        self.beamng.stop_scenario()

    def start_scenario(self):
        logging.info('start_scenario')
        self.beamng.start_scenario()
        self.vehicle.ai_set_mode('span')
        self.vehicle.ai_drive_in_lane(lane=True)
        self.vehicle.ai_set_aggression(0.5)
        self.vehicle.set_color(rgba=(0, 0, 1, 0.5))
        self.vehicle.ai_set_speed(12)
        self.vehicle.ai_set_waypoint('end_point')

    def load_scenario(self, test: Test):
        logging.info('load_scenario')
        self.scenario = Scenario('tig', 'example')
        road = Road(material='tig_road_rubber_sticky', rid='flat_road', interpolate=True)

        # Ensure not overriding the test object (copy first the whole list)
        road_nodes = test.interpolated_road_points.copy()
        for road_node in road_nodes:
            road_node.extend([-28, 10])

        road.nodes.extend(road_nodes)

        self.scenario.add_road(road)

        self.vehicle = Vehicle(vid='ego_vehicle', model='etk800', licence='Scissor')
        electrics = Electrics()
        self.vehicle.attach_sensor('electrics', electrics)

        x_start, y_start, z_start, x_dir, y_dir, alpha = self.__compute_start_position(road_nodes)
        # TODO: Calculate the start rotation of the car in quaterion
        rot_quat = (0, 0, 1, -0.1)
        rot = (0, 0, alpha / (2 * math.pi))
        self.scenario.add_vehicle(self.vehicle, pos=(x_start, y_start, z_start), rot_quat=rot_quat)

        end_point = road_nodes[-1][:3]

        self.scenario.add_checkpoints(positions=[end_point], scales=[(5, 5, 5)], ids=['end_point'])
        self.scenario.make(self.beamng)
        self.beamng.load_scenario(self.scenario)

    def update_car(self):
        logging.info('update_car')
        self.vehicle.update_vehicle()
        _ = self.beamng.poll_sensors(self.vehicle)  # otherwise, the values are not updated (bug of beamngpy)
        self.car_state = self.vehicle.state

    def get_car_position(self):
        logging.info('get_car_position')
        x_pos = self.car_state['pos'][0]
        y_pos = self.car_state['pos'][1]
        z_pos = self.car_state['pos'][2]
        return x_pos, y_pos, z_pos

    @staticmethod
    def __compute_start_position(road_nodes):
        logging.info('compute_start_position')
        first_road_point = road_nodes[0]
        second_road_point = road_nodes[1]
        x_dir, y_dir = (second_road_point[0] - first_road_point[1], second_road_point[1] - first_road_point[1])
        x_dir_norm, y_dir_norm = (x_dir / math.sqrt(x_dir ** 2 + y_dir ** 2),
                                  y_dir / math.sqrt(x_dir ** 2 + y_dir ** 2))
        alpha = math.asin(y_dir_norm)

        x_cross_dir_norm, y_cross_dir_norm = y_dir_norm, -x_dir_norm

        return first_road_point[0] + 2.5 * x_cross_dir_norm, first_road_point[
            1] + 2.5 * y_cross_dir_norm, -28.0, x_dir, y_dir, alpha


if __name__ == '__main__':
    logging.info('beamng_simulator.py')
