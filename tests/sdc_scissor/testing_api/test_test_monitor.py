import logging

from sdc_scissor.testing_api.test_monitor import TestMonitor


class TestTestMonitor:
    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    def setup_method(self):
        self.test_monitor = TestMonitor(simulator=None, test=None, oob=None, road_model=None)

    def test_is_car_moving_car_stays_on_same_position(self):
        self.test_monitor.data = [(0, 0, 0, 0), (5, 0, 0, 0)]
        expected = False
        actual = self.test_monitor.is_car_moving()
        assert expected == actual

    def test_is_car_moving_car_stays_not_on_same_position(self):
        self.test_monitor.data = [(0, 0, 0, 0), (5, 10, 10, 0)]
        expected = True
        actual = self.test_monitor.is_car_moving()
        assert expected == actual

    def test_is_car_moving_not_enough_sim_data_yet_to_make_decision(self):
        self.test_monitor.data = [(0, 0, 0, 0), (0.1, 0, 0, 0)]
        expected = True
        actual = self.test_monitor.is_car_moving()
        assert expected == actual


if __name__ == '__main__':
    logging.info('test_test_monitor.py')
