from sdc_scissor.simulator_api.beamng_simulator import BeamNGSimulator


class TestBeamNGSimulator:
    def test_open_beamng(self, mocker):
        beamng_mock = mocker.patch("beamngpy.BeamNGpy")
        beamng_mock.open.return_value = None

        beamng_simulator = BeamNGSimulator(beamng=beamng_mock, rf=1.5, max_speed=120, fov=120)
        beamng_simulator.open()
