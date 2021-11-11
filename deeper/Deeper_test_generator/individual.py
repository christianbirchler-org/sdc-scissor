from typing import Tuple

from deeper.Deeper_test_generator.member import Member


class Individual:
    def __init__(self, m1: Member):
        self.m1: Member = m1
        self.members_distance: float = None
        self.oob_ff: float = None
        self.seed: Member = None

    def clone(self) -> 'creator.base':
        raise NotImplemented()

    def evaluate(self):
        raise NotImplemented()

    def mutate(self):
        raise NotImplemented()

    def distance(self, i2: 'Individual'):
        i1 = self
        a = i1.m1.distance(i2.m1)

        dist = a
        return dist

    def semantic_distance(self, i2: 'Individual'):
        raise NotImplemented()

    def members_by_sign(self) -> Tuple[Member, Member]:
        msg = 'distance metric'
        assert self.m1.distance_to_boundary, msg

        result = self.members_by_distance_to_boundary()
        return result

    def members_by_distance_to_boundary(self):
        def dist(m: Member):
            return m.distance_to_boundary
        result = self.m1
        return result
