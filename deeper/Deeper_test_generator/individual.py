from typing import Tuple
import abc

from deeper.Deeper_test_generator.member import Member


class Individual(abc.ABC):
    def __init__(self, m1: Member):
        self.m1: Member = m1
        self.members_distance: float = None
        self.oob_ff: float = None
        self.seed: Member = None

    @abc.abstractmethod
    def clone(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def evaluate(self, executor):
        raise NotImplementedError()

    @abc.abstractmethod
    def mutate(self):
        raise NotImplementedError()

    def distance(self, i2: 'Individual'):
        i1 = self
        a = i1.m1.distance(i2.m1)

        dist = a
        return dist

    @abc.abstractmethod
    def semantic_distance(self, i2: 'Individual'):
        raise NotImplementedError()

    def members_by_sign(self) -> Tuple[Member, Member]:
        msg = 'distance metric'
        assert self.m1.distance_to_boundary, msg

        result = self.members_by_distance_to_boundary()
        return result

    def members_by_distance_to_boundary(self):
        result = self.m1
        return result
