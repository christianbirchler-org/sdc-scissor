from typing import Dict


class Member:
    def __init__(self):
        self.distance_to_boundary: float = None

    def distance(self, o: 'Member'):
        raise NotImplemented()

    def clone(self):
        raise NotImplemented()

    def evaluate(self):
        raise NotImplemented()

    def to_tuple(self):
        raise NotImplemented()

    def mutate(self):
        raise NotImplemented()

    def to_dict(self) -> dict:
        raise NotImplemented()

    @classmethod
    def from_dict(cls, dict: Dict):
        raise NotImplemented()
