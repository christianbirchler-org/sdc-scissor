from sdc_scissor.can_api.can_bus_handler import NoCANBusOutput
from sdc_scissor.config import CONFIG
from sdc_scissor.testing_api.test_runner import TestRunner


class TestTestRunner:
    def setup_class(self):
        CONFIG.config = {"canbus": False, "can_dbc": "", "can_dbc_map": "", "can_interface": "", "can_bitrate": ""}

    def test_single_test_run_with_obstacles_and_car_is_out_of_lane(self, mocker):
        test_runner = TestRunner()

        test_runner.can_output = NoCANBusOutput()
        test_runner.test_loader = mocker.patch("sdc_scissor.testing_api.test_loader.TestLoader")
        test_runner.ml_component = mocker.stub()
        test_runner.simulator = mocker.patch("sdc_scissor.simulator_api.abstract_simulator.AbstractSimulator")
        test_runner.simulator.get_car_position.return_value = 10, 1, 1
        test_runner.oob = 0.5
        test_runner.interrupt = True
        test_runner.bump_dist = 20
        test_runner.delineator_dist = 20
        test_runner.tree_dist = 20
        test_runner.obstacle_factory = mocker.patch("sdc_scissor.obstacle_api.obstacle_factory.ObstacleFactory")
        test_runner.fov = 120

        test = mocker.patch("sdc_scissor.testing_api.test.Test")
        test.interpolated_road_points = [[1, 1], [200, 200]]
        test_monitor = mocker.patch("sdc_scissor.testing_api.test_monitor.TestMonitor")
        test_monitor.test = test
        test_runner.test_monitor = test_monitor
        test_runner.run(test)

    def test_run_test_suite_simple(self, mocker):
        test = mocker.patch("sdc_scissor.testing_api.test.Test")
        test.interpolated_road_points = [[1, 1], [200, 200]]

        test_runner = TestRunner()

        test_runner.can_output = NoCANBusOutput()
        test_runner.test_loader = mocker.patch("sdc_scissor.testing_api.test_loader.TestLoader")
        test_runner.test_loader.has_next.side_effect = [True, False]
        test_runner.test_loader.next.return_value = test, mocker.stub()
        test_runner.ml_component = mocker.stub()
        test_runner.simulator = mocker.patch("sdc_scissor.simulator_api.abstract_simulator.AbstractSimulator")
        test_runner.simulator.get_car_position.return_value = 10, 1, 1
        test_runner.oob = 0.5
        test_runner.interrupt = True
        test_runner.bump_dist = 20
        test_runner.delineator_dist = 20
        test_runner.tree_dist = 20
        test_runner.obstacle_factory = mocker.patch("sdc_scissor.obstacle_api.obstacle_factory.ObstacleFactory")
        test_runner.fov = 120
        test_monitor = mocker.patch("sdc_scissor.testing_api.test_monitor.TestMonitor")
        test_monitor.test = test
        test_runner.test_monitor = test_monitor

        test_runner.run_test_suite()

    def test_run_test_suite_with_raising_exception(self, mocker):
        test = mocker.patch("sdc_scissor.testing_api.test.Test")
        test.interpolated_road_points = [[1, 1], [200, 200]]
        test.save_as_json.side_effect = [Exception(), None, None, None]

        test_runner = TestRunner()

        test_runner.can_output = NoCANBusOutput()
        test_runner.test_loader = mocker.patch("sdc_scissor.testing_api.test_loader.TestLoader")
        test_runner.test_loader.has_next.side_effect = [True, True, True, False]
        test_runner.test_loader.next.return_value = test, mocker.stub()
        test_runner.ml_component = mocker.stub()
        test_runner.simulator = mocker.patch("sdc_scissor.simulator_api.abstract_simulator.AbstractSimulator")
        test_runner.simulator.get_car_position.return_value = 10, 1, 1
        test_runner.oob = 0.5
        test_runner.interrupt = True
        test_runner.bump_dist = 20
        test_runner.delineator_dist = 20
        test_runner.tree_dist = 20
        test_runner.obstacle_factory = mocker.patch("sdc_scissor.obstacle_api.obstacle_factory.ObstacleFactory")
        test_runner.fov = 120
        test_monitor = mocker.patch("sdc_scissor.testing_api.test_monitor.TestMonitor")
        test_monitor.test = test
        test_runner.test_monitor = test_monitor

        test_runner.run_test_suite()
