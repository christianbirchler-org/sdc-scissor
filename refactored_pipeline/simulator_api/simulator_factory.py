import logging
import abc
import time

from beamngpy import BeamNGpy, Scenario


class AbstractSimulator(abc.ABC):
    def __init__(self):
        super().__init__()
        self.equipments = {}

    @abc.abstractmethod
    def open(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass

    @abc.abstractmethod
    def create_new_instance(self):
        pass

    @abc.abstractmethod
    def start_scenario(self):
        pass

    @abc.abstractmethod
    def load_scenario(self, scenario):
        pass

    @abc.abstractmethod
    def update_sensors(self):
        pass


class BeamNGSimulator(AbstractSimulator):
    def __init__(self, host: str, port: int, home: str, user: str):
        super().__init__()
        self.host = host
        self.port = port
        self.home = home
        self.user = user
        self.beamng = BeamNGpy(host, port, home=home, user=user)

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

    def start_scenario(self):
        self.beamng.start_scenario()
        self.vehicle.ai_set_mode('span')
        self.vehicle.ai_drive_in_lane(lane=True)
        self.vehicle.ai_set_aggression(0.5)
        self.vehicle.set_color(rgba=(0, 0, 1, 0.5))
        self.vehicle.ai_set_speed(12)
        self.vehicle.ai_set_waypoint('end_point')
        # self.vehicle.start_in_game_logging(outputDir='./')

    def load_scenario(self, test: Test):
        logging.info('* load_scenario')
        scenario = Scenario('tig', 'example')
        road = Road(material='tig_road_rubber_sticky', rid='flat_road', interpolate=True)
        road.nodes.extend(test.interpolated_points)

        scenario.add_road(road)

        self.vehicle = Vehicle(vid='ego_vehicle', model='etk800', licence='Scissor')
        electrics = Electrics()
        self.vehicle.attach_sensor('electrics', electrics)

        x_start, y_start, z_start, x_dir, y_dir, alpha = self.__compute_start_position(test)
        # TODO: Calculate the start rotation of the car in quaterion
        rot_quat = (0, 0, 1, -0.1)
        rot = (0, 0, alpha / (2 * math.pi))
        scenario.add_vehicle(self.vehicle, pos=(x_start, y_start, z_start), rot_quat=rot_quat)

        end_point = test.interpolated_points[-1][:3]

        scenario.add_checkpoints(positions=[end_point], scales=[(5, 5, 5)], ids=['end_point'])
        scenario.make(self.beamng)
        self.beamng.load_scenario(scenario)

    def update_sensors(self):
        pass

    @staticmethod
    def __compute_start_position(test: Test):
        logging.info('* compute_start_position')
        first_road_point = test.interpolated_points[0]
        second_road_point = test.interpolated_points[1]
        x_dir, y_dir = (second_road_point[0] - first_road_point[1], second_road_point[1] - first_road_point[1])
        x_dir_norm, y_dir_norm = (x_dir / sqrt(x_dir ** 2 + y_dir ** 2), y_dir / sqrt(x_dir ** 2 + y_dir ** 2))
        alpha = math.asin(y_dir_norm)

        x_cross_dir_norm, y_cross_dir_norm = y_dir_norm, -x_dir_norm

        return first_road_point[0] + 2.5 * x_cross_dir_norm, first_road_point[
            1] + 2.5 * y_cross_dir_norm, -28.0, x_dir, y_dir, alpha


class SimulatorFactory:
    @staticmethod
    def get_beamng_simulator() -> AbstractSimulator:
        beamng_simulator = BeamNGSimulator(
            host='localhost',
            port=64256,
            home=r'C:\Users\birc\Documents\BeamNG.tech.v0.24.0.2\BeamNG.drive-0.24.0.2.13392',
            user=r'C:\Users\birc\Documents\BeamNG.drive'
        )
        return beamng_simulator


if __name__ == '__main__':
    logging.info('* simulator_factory.py')
