from beamngpy import BeamNGpy, Vehicle

from refactored_pipeline.testing_api.test import Test


class TestMonitor:
    def __init__(self, simulator: BeamNGpy, vehicle: Vehicle, test: Test):
        self.simulator = simulator
        self.vehicle = vehicle
        self.test = test
        self.is_finished = False
        self.car_is_out_of_lane = False
        self.road = None

    def check(self):
        print('* check')
        self.vehicle.update_vehicle()
        sensors = self.simulator.poll_sensors(self.vehicle)
        state = self.vehicle.state
        x_pos = state['pos'][0]
        y_pos = state['pos'][1]
        print('** x: {}\ny: {}\n\n'.format(x_pos, y_pos))


if __name__ == '__main__':
    print('* test_monitor.py')
