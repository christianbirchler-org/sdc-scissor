import numpy as np

import sdc_scissor.simulator_api.beamng_simulator as bs
from sdc_scissor.simulator_api.beamng_simulator import BeamNGSimulator


class TestBeamNGSimulator:
    def test_open_beamng(self, mocker):
        beamng_mock = mocker.patch("beamngpy.BeamNGpy")
        beamng_mock.open.return_value = None

        beamng_simulator = BeamNGSimulator(beamng=beamng_mock, rf=1.5, max_speed=120, fov=120)
        beamng_simulator.open()

    def test_close_beamng(self, mocker):
        beamng_mock = mocker.patch("beamngpy.BeamNGpy")

        beamng_simulator = BeamNGSimulator(beamng=beamng_mock, rf=1.5, max_speed=120, fov=120)
        beamng_simulator.close()

    def test_create_new_instance(self, mocker, fs):
        fs.makedir("./home")
        fs.create_file("./home/Bin64/BeamNG.drive.x64.exe")
        fs.makedir("./user")

        beamng_mock = mocker.patch("beamngpy.BeamNGpy")
        beamng_mock.home = "./home"
        beamng_mock.user = "./user"

        beamng_simulator = BeamNGSimulator(beamng=beamng_mock, rf=1.5, max_speed=120, fov=120)
        beamng_simulator.create_new_instance()

    def test_load_scenario(self, mocker, fs):
        test_mock = mocker.patch("sdc_scissor.testing_api.test.Test")
        test_mock.interpolated_road_points = [[1, 1], [100, 100]]

        mock_bump = mocker.patch("sdc_scissor.obstacle_api.bump.Bump")
        mock_bump.obstacle_type = "procedural"
        mock_tree = mocker.patch("sdc_scissor.obstacle_api.tree.Tree")
        mock_tree.obstacle_type = "static"

        mock_obstacles = [mock_bump, mock_tree]

        mock_scenario = mocker.patch("beamngpy.Scenario")

        fs.makedir("./home")
        fs.create_file("./home/Bin64/BeamNG.drive.x64.exe")
        fs.makedir("./user")

        beamng_mock = mocker.patch("beamngpy.BeamNGpy")
        beamng_mock.home = "./home"
        beamng_mock.user = "./user"

        beamng_simulator = BeamNGSimulator(beamng=beamng_mock, rf=1.5, max_speed=120, fov=120)
        beamng_simulator.load_scenario(test_mock, mock_scenario, mock_obstacles)

    def test_start_orientation_among_positive_x(self):
        road_points = [[0, 0, 0], [50, 0, 0]]
        _, alpha = bs._compute_start_position(road_nodes=road_points)
        actual = alpha
        expected_1 = 0
        expected_2 = np.pi
        tol = 0.01
        assert (expected_1 - tol < actual < expected_1 + tol) or (expected_2 - tol < actual < expected_2 + tol)

    def test_start_orientation_among_negative_x(self):
        road_points = [[50, 0, 0], [0, 0, 0]]
        _, alpha = bs._compute_start_position(road_nodes=road_points)
        actual = alpha
        expected_1 = 0
        expected_2 = np.pi
        tol = 0.01
        assert (expected_1 - tol < actual < expected_1 + tol) or (expected_2 - tol < actual < expected_2 + tol)
