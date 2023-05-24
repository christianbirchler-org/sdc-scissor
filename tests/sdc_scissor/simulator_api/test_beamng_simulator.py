from sdc_scissor.simulator_api.beamng_simulator import BeamNGSimulator


@pytest.mark.skip()
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
