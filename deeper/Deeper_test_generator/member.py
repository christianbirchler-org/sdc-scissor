from typing import Dict
import abc


class Member(abc.ABC):
    def __init__(self):
        self.distance_to_boundary: float = None

    @abc.abstractmethod
    def distance(self, other: 'Member'):
        raise NotImplementedError()

    @abc.abstractmethod
    def clone(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def evaluate(self, executor):
        raise NotImplementedError()

    @abc.abstractmethod
    def to_tuple(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def mutate(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, data_dict: Dict):
        raise NotImplementedError()
