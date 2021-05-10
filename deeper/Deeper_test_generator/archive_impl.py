from itertools import permutations
from typing import List, Tuple
import logging as log

from deeper.Deeper_test_generator.archive import Archive
from deeper.Deeper_test_generator.individual import Individual
from deeper.Deeper_test_generator.misc import closest_elements


class GreedyArchive(Archive):
    def process_population(self, pop: List[Individual]):
        for candidate in pop:
            if candidate.oob_ff < 0 and candidate.m1.distance_to_boundary < (-0.5):
                self.add(candidate)


class NonGreedyArchive(Archive):
    def __init__(self, ARCHIVE_THRESHOLD):
        super().__init__()
        self.ARCHIVE_THRESHOLD = ARCHIVE_THRESHOLD

    def process_population(self, pop: List[Individual]):
        for candidate in pop:
            assert candidate.oob_ff, candidate.name
            if candidate.oob_ff < 0 and candidate.m1.distance_to_boundary < (-0.5):
                if len(self) == 0:
                    self._int_add(candidate)
                    log.debug('add initial individual')
                else:
                    # uses semantic_distance to exploit behavioral information
                    closest_archived, candidate_archived_distance = \
                        closest_elements(self, candidate, lambda a, b: a.semantic_distance(b))[0]
                    closest_archived: Individual

                    if candidate_archived_distance > self.ARCHIVE_THRESHOLD:
                        log.debug('candidate is far from any archived individual')
                        self._int_add(candidate)
                    else:
                        log.debug('candidate is very close to an archived individual')
                        #self._int_add(candidate)
                        #print('Added to archive:', closest_archived)


    def _int_add(self, candidate):
        self.add(candidate)
        print('archive add', candidate)


