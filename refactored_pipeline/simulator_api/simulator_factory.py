from beamngpy import BeamNGpy


class SimulatorFactory:
    @staticmethod
    def get_beamng_simulator() -> BeamNGpy:
        beamng = BeamNGpy('localhost', 64256,
                          home=r'C:\Users\birc\Documents\BeamNG.tech.v0.24.0.2\BeamNG.drive-0.24.0.2.13392',
                          user=r'C:\Users\birc\Documents\BeamNG.drive')
        return beamng


if __name__ == '__main__':
    logging.info('* simulator_factory.py')
