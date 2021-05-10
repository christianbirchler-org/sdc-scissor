from typing import List

from deeper.Deeper_test_generator.individual import Individual


class IndividualSet(set):
    pass


class Archive(IndividualSet):
    def process_population(self, pop: List[Individual]):
        raise NotImplemented()