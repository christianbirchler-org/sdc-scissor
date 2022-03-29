import time

from beamngpy import BeamNGpy, Scenario, Vehicle, Road
from beamngpy.sensors import Electrics

from refactored_pipeline.testing_api.test_loader import TestLoader
from refactored_pipeline.testing_api.test import Test
from refactored_pipeline.testing_api.test_monitor import TestMonitor


class TestRunner:
    def __init__(self, **kwargs) -> None:
        self.test_loader: TestLoader = kwargs.get('test_loader', None)
        self.ml_component = kwargs.get('machine_learning_api', None)
        self.simulator: BeamNGpy = kwargs.get('simulator', None)

    def run(self, test: Test) -> None:
        """
        Runs the test with the simulator given by instantiation of the test runner.
        """
        print('* run')

        for road_point in test.interpolated_points:
            road_point.extend([-28, 10])

        print(test.interpolated_points)
        self.simulator.open()
        scenario = Scenario('tig', 'example')

        road = Road(material='tig_road_rubber_sticky', rid='flat_road', interpolate=True)
        road.nodes.extend(test.interpolated_points)

        scenario.add_road(road)

        vehicle = Vehicle(vid='ego_vehicle', model='etk800', licence='Scissor')
        electrics = Electrics()
        vehicle.attach_sensor('electrics', electrics)

        scenario.add_vehicle(vehicle, pos=(-2.5, 0, -28.0))

        scenario.make(self.simulator)

        self.simulator.load_scenario(scenario)
        self.simulator.start_scenario()

        vehicle.ai_set_mode('span')
        vehicle.ai_drive_in_lane(lane=True)
        vehicle.ai_set_aggression(0.5)
        vehicle.set_color(rgba=(0, 0, 1, 0.5))
        vehicle.ai_set_speed(12)

        test_monitor = TestMonitor(self.simulator, vehicle, test)
        while not test_monitor.is_finished:
            test_monitor.check()
            time.sleep(0.1)

        input('Hit enter...')


if __name__ == '__main__':
    print('* test_runner.py')
