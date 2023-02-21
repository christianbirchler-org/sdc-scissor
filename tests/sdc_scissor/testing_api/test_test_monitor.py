import logging

from sdc_scissor.testing_api.test_monitor import TestMonitor


class TestTestMonitor:
    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    def setup_method(self):
        self.test_monitor = TestMonitor(
            simulator=None, test=None, oob=None, road_model=None
        )
        self.test_monitor.start_timer()

    def test_is_car_moving_car_stays_on_same_position(self, mocker):
        self.test_monitor.test = mocker.patch("sdc_scissor.testing_api.test.Test")
        simulation_data_entry_t0 = {"time": 0, "position": (0, 0, 0)}
        simulation_data_entry_t1 = {"time": 11, "position": (0, 0, 0)}
        self.test_monitor.test.simulation_data = [
            simulation_data_entry_t0,
            simulation_data_entry_t1,
        ]
        expected = False
        actual = self.test_monitor.is_car_moving()
        assert expected == actual

    def test_is_car_moving_car_stays_not_on_same_position(self, mocker):
        self.test_monitor.test = mocker.patch("sdc_scissor.testing_api.test.Test")
        simulation_data_entry_t0 = {"time": 0, "position": (0, 0, 0)}
        simulation_data_entry_t1 = {"time": 5, "position": (10, 10, 0)}
        self.test_monitor.test.simulation_data = [
            simulation_data_entry_t0,
            simulation_data_entry_t1,
        ]
        expected = True
        actual = self.test_monitor.is_car_moving()
        assert expected == actual

    def test_is_car_moving_not_enough_sim_data_yet_to_make_decision(self, mocker):
        self.test_monitor.test = mocker.patch("sdc_scissor.testing_api.test.Test")
        simulation_data_entry_t0 = {"time": 0, "position": (0, 0, 0)}
        simulation_data_entry_t1 = {"time": 0.1, "position": (0, 0, 0)}
        self.test_monitor.test.simulation_data = [
            simulation_data_entry_t0,
            simulation_data_entry_t1,
        ]
        expected = True
        actual = self.test_monitor.is_car_moving()
        assert expected == actual

    def test_check_verify_if_test_is_finished(self, mocker):
        mock_simulator = mocker.patch(
            "sdc_scissor.simulator_api.abstract_simulator.AbstractSimulator"
        )
        mock_simulator.update_car.return_value = None
        mock_simulator.get_car_position.return_value = 0, 0, 0
        self.test_monitor.simulator = mock_simulator

        mock_test = mocker.patch("sdc_scissor.testing_api.test.Test")
        mock_test.interpolated_road_points = [[0, 0, 0], [1, 1, 0]]
        self.test_monitor.test = mock_test

        self.test_monitor.process_car_state(interrupt_on_failure=True)
        expected = True
        actual = self.test_monitor.is_test_finished
        assert expected == actual


if __name__ == "__main__":
    logging.info("test_test_monitor.py")
