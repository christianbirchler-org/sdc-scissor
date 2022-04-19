import logging

from sdc_scissor.simulator_api.abstract_simulator import AbstractSimulator
from sdc_scissor.simulator_api.beamng_simulator import BeamNGSimulator


class SimulatorFactory:
    @staticmethod
    def get_beamng_simulator(home, user, rf: float, max_speed: float) -> AbstractSimulator:
        beamng_simulator = BeamNGSimulator(
            host='localhost',
            port=64256,
            home=home,
            user=user,
            rf=rf,
            max_speed=max_speed
        )
        return beamng_simulator


if __name__ == '__main__':
    logging.info('* simulator_factory.py')
