import itertools
import json
import random
from typing import List

from deap import creator

from code_pipeline.tests_generation import RoadTestFactory
from deeper.Deeper_test_generator.archive import Archive
from deeper.Deeper_test_generator.archive_impl import NonGreedyArchive
from deeper.Deeper_test_generator.folders import folders
from deeper.Deeper_test_generator.log_setup import get_logger
from deeper.Deeper_test_generator.member import Member
from deeper.Deeper_test_generator.metrics import get_radius_seed, get_diameter
from deeper.Deeper_test_generator.misc import delete_folder_recursively
from deeper.Deeper_test_generator.problem import Problem
from deeper.Deeper_test_generator.seed_pool_access_strategy import SeedPoolAccessStrategy
from deeper.Deeper_test_generator.seed_pool_impl import SeedPoolFolder, SeedPoolRandom
from deeper.Deeper_test_generator.beamng_config import BeamNGConfig
from deeper.Deeper_test_generator.beamng_evaluator import BeamNGEvaluator
from deeper.Deeper_test_generator.beamng_individual import BeamNGIndividual
from deeper.Deeper_test_generator.beamng_individual_set_store import BeamNGIndividualSetStore
from deeper.Deeper_test_generator.beamng_member import BeamNGMember
from deeper.Deeper_test_generator.road_generator2 import RoadGenerator

log = get_logger(__file__)


class BeamNGProblem(Problem):
    def __init__(self, executor, config: BeamNGConfig, archive=None):
        self.executor = executor
        self.config: BeamNGConfig = config
        self._evaluator: BeamNGEvaluator = None
        super().__init__(config, archive)
        if self.config.generator_name == self.config.GEN_RANDOM:
            seed_pool = SeedPoolRandom(self, config.POPSIZE)
        else:
            seed_pool = SeedPoolFolder(self, config.seed_folder)
        self._seed_pool_strategy = SeedPoolAccessStrategy(seed_pool)
        self.experiment_path = folders.experiments.joinpath(self.config.experiment_name)
        delete_folder_recursively(self.experiment_path)

    def deap_generate_individual(self):
        seed = self._seed_pool_strategy.get_seed()

        road1 = seed
        #road1 = seed.clone().mutate()

        road1.config = self.config

        individual: BeamNGIndividual = creator.Individual(road1, self.config, self.archive)
        individual.seed = seed
        log.info(f'Generated {individual}')

        return individual

    def deap_evaluate_individual(self, individual: BeamNGIndividual):
        return individual.evaluate(self.executor)

    def on_iteration(self, idx, pop: List[BeamNGIndividual], logbook):
        self.experiment_path.mkdir(parents=True, exist_ok=True)
        self.experiment_path.joinpath('config.json').write_text(json.dumps(self.config.__dict__))

        gen_path = self.experiment_path.joinpath(f'gen{idx}')
        gen_path.mkdir(parents=True, exist_ok=True)

        # Generate final report at the end of the last iteration.
        if idx + 1 == self.config.NUM_GENERATIONS:
            report = {
                'archive_len': len(self.archive),
                'radius': get_radius_seed(self.archive),
                'diameter_out': get_diameter([ind.members_by_sign()[0] for ind in self.archive]),
                'diameter_in': get_diameter([ind.members_by_sign()[1] for ind in self.archive])
            }
            gen_path.joinpath(f'report{idx}.json').write_text(json.dumps(report))

        BeamNGIndividualSetStore(gen_path.joinpath('population')).save(pop)
        BeamNGIndividualSetStore(gen_path.joinpath('archive')).save(self.archive)

    def generate_random_member(self) -> Member:
        result = RoadGenerator(num_control_nodes=self.config.num_control_nodes, max_angle=self.config.MAX_ANGLE, seg_length=self.config.SEG_LENGTH,
                               num_spline_nodes=self.config.NUM_SPLINE_NODES).generate()

        result.config = self.config
        result.problem = self
        return result

    def deap_individual_class(self):
        return BeamNGIndividual

    def member_class(self):
        return BeamNGMember

    def reseed(self, pop, offspring):
        if len(self.archive) > 0:
            stop = self.config.RESEED_UPPER_BOUND + 1
            seed_range = min(random.randrange(0, stop), len(pop))
            archived_seeds = [i.seed for i in self.archive]
            for i in range(len(pop)):
                if pop[i].seed in archived_seeds:
                    ind1 = self.deap_generate_individual()
                    pop[i] = ind1

    def _get_evaluator(self):
        if self._evaluator:
            return self._evaluator

        self._evaluator = self.executor

        return self._evaluator

    def pre_evaluate_members(self, individuals: List[BeamNGIndividual]):
        all_members = list(itertools.chain([(ind.m1) for ind in individuals]))
        log.info('----Initial Evaluation----')
        for member in all_members:
            road_points = [(node[0], node[1]) for node in member.sample_nodes]
            the_test = RoadTestFactory.create_road_test(road_points)
            log.info("Evaluating %s", member.name)
            test_outcome, description, execution_data, min_oob_distance = self.executor.execute_test(the_test)
            member.distance_to_boundary = min_oob_distance
            log.info("Outcome %s", test_outcome)
            if test_outcome != "INVALID":
                log.info("Minimum oob_Distance %s", min_oob_distance)

        log.info('----End of Initial Evaluation----')
