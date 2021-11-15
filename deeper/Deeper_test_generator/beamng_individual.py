from deap import creator

from deeper.Deeper_test_generator.config import Config
from deeper.Deeper_test_generator.log_setup import get_logger
from deeper.Deeper_test_generator.archive import Archive
from deeper.Deeper_test_generator.individual import Individual
from deeper.Deeper_test_generator.beamng_member import BeamNGMember

log = get_logger(__file__)


class BeamNGIndividual(Individual):
    counter = 0

    def __init__(self, m1: BeamNGMember, m2: BeamNGMember, config: Config, archive: Archive):
        super().__init__(m1)
        self.m1: BeamNGMember = self.m1
        self.m2: BeamNGMember = m2
        BeamNGIndividual.counter += 1
        self.name = f'Road{str(BeamNGIndividual.counter)}'
        self.name_ljust = self.name.ljust(6)
        self.config = config
        self.archive = archive
        self.m1.parent = self
        self.sparseness = None
        self.aggregate = None
        self.seed: BeamNGMember
        self.ff1 = None

    def evaluate(self, executor):
        log.info(f'Evaluating {self.name}')
        self.m1.evaluate(executor)
        self.oob_ff = self.m1.distance_to_boundary
        self.ff1 = 1.00 / self.m1.length
        return self.ff1, self.oob_ff

    def clone(self) -> 'BeamNGIndividual':
        res: BeamNGIndividual = creator.Individual(self.m1.clone(), self.config, self.archive)
        res.seed = self.seed
        # log.info(f'cloned to {res} from {self}')
        log.info('cloning done')
        return res

    def semantic_distance(self, i2: 'BeamNGIndividual'):

        i1 = self

        i1_posi = i1.members_by_sign()
        i2_posi = i2.members_by_sign()

        return i1_posi.distance(i2_posi)

    def _assert_members_not_equals(self):
        assert self.m1.control_nodes != self.m2.control_nodes

    def to_dict(self):
        return {'name': self.name,
                'members_distance': self.members_distance,
                'm1': self.m1.to_dict(),
                'seed': self.seed.to_dict()}

    @staticmethod
    def from_dict(d):
        m1 = BeamNGMember.from_dict(d['m1'])
        m2 = BeamNGMember.from_dict(d['m2'])
        ind = BeamNGIndividual(m1, m2, None, None)
        ind.members_distance = d['members_distance']
        ind.name = d['name']
        return ind

    def __str__(self):
        return f'{self.name_ljust}'

    def mutate(self):
        road_to_mutate = self.m1
        condition = False
        while not condition:
            road_to_mutate.mutate()
            condition = True
        self.members_distance = None
        log.info(f'{self} Mutated')
