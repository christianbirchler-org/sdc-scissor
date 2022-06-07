import logging

from sdc_scissor.obstacle_api.bump import Bump
from sdc_scissor.obstacle_api.beamng_bump import BeamngBump
from sdc_scissor.obstacle_api.delineator import Delineator
from sdc_scissor.obstacle_api.beamng_delineator import BeamngDelineator
from sdc_scissor.obstacle_api.obstacle_factory import ObstacleFactory


class BeamngObstacleFactory(ObstacleFactory):
    def create_bump(self) -> Bump:
        return BeamngBump()

    def create_delineator(self) -> Delineator:
        return BeamngDelineator()


if __name__ == "__main__":
    logging.info("beamng_obstacle_factory.py")
