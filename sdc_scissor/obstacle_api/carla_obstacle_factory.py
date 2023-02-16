import logging

from sdc_scissor.obstacle_api.bump import Bump
from sdc_scissor.obstacle_api.carla_bump import CarlaBump
from sdc_scissor.obstacle_api.carla_delineator import CarlaDelineator
from sdc_scissor.obstacle_api.carla_tree import CarlaTree
from sdc_scissor.obstacle_api.delineator import Delineator
from sdc_scissor.obstacle_api.obstacle_factory import ObstacleFactory
from sdc_scissor.obstacle_api.tree import Tree


class CarlaObstacleFactory(ObstacleFactory):
    def create_bump(self) -> Bump:
        return CarlaBump()

    def create_delineator(self) -> Delineator:
        return CarlaDelineator()

    def create_tree(self) -> Tree:
        return CarlaTree()


if __name__ == "__main__":
    logging.info("carla_obstacle_factory.py")
