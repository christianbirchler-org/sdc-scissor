import abc
import logging

from sdc_scissor.obstacle_api.bump import Bump
from sdc_scissor.obstacle_api.delineator import Delineator
from sdc_scissor.obstacle_api.tree import Tree


class ObstacleFactory(abc.ABC):
    @abc.abstractmethod
    def create_bump(self) -> Bump:
        pass

    @abc.abstractmethod
    def create_delineator(self) -> Delineator:
        pass

    @abc.abstractmethod
    def create_tree(self) -> Tree:
        pass


if __name__ == "__main__":
    logging.info("abstract_obstacle_factory.py")
