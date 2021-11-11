from typing import Dict


class Member:
    def __init__(self):
        self.distance_to_boundary: float = None

    def distance(self, o: 'Member'):
        raise NotImplementedError()

    def clone(self):
        raise NotImplementedError()

    def evaluate(self):
        raise NotImplementedError()

    def to_tuple(self):
        raise NotImplementedError()

    def mutate(self):
        raise NotImplementedError()

    def to_dict(self) -> dict:
        raise NotImplementedError()

    @classmethod
    def from_dict(cls, dict: Dict):
        raise NotImplementedError()
