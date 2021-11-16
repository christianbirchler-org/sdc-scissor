from typing import List
import abc

from deeper.Deeper_test_generator.config import Config
from deeper.Deeper_test_generator.archive import Archive
from deeper.Deeper_test_generator.individual import Individual
from deeper.Deeper_test_generator.member import Member


class Problem(abc.ABC):
    def __init__(self, config: Config, archive: Archive):
        self.config: Config = config
        self.archive = archive

    @abc.abstractmethod
    def deap_generate_individual(self) -> Individual:
        raise NotImplementedError()

    @staticmethod
    def deap_mutate_individual(individual: Individual):
        individual.mutate()

    @abc.abstractmethod
    def deap_evaluate_individual(self, individual: Individual):
        raise NotImplementedError()

    @abc.abstractmethod
    def deap_individual_class(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def on_iteration(self, idx, pop: List[Individual]):
        raise NotImplementedError()

    @abc.abstractmethod
    def member_class(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def reseed(self, population):
        raise NotImplementedError()

    @abc.abstractmethod
    def generate_random_member(self) -> Member:
        raise NotImplementedError()

    @abc.abstractmethod
    def pre_evaluate_members(self, individuals: List[Individual]):
        pass
