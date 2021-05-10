import hashlib
import random
from typing import Tuple, Dict

from code_pipeline.tests_generation import RoadTestFactory
from deeper.Deeper_test_generator.beamng_config import BeamNGConfig
from deeper.Deeper_test_generator.beamng_evaluator import BeamNGEvaluator
from deeper.Deeper_test_generator.member import Member
from deeper.Deeper_test_generator.catmull_rom import catmull_rom
from deeper.Deeper_test_generator.road_bbox import RoadBoundingBox
from self_driving.road_polygon import RoadPolygon
from self_driving.edit_distance_polyline import iterative_levenshtein
from deeper.Deeper_test_generator.log_setup import get_logger
from deeper.Deeper_test_generator.road_generator2 import RoadGenerator


Tuple4F = Tuple[float, float, float, float]
Tuple2F = Tuple[float, float]

log = get_logger(__file__)

class BeamNGMember(Member):

    counter = 0

    def __init__(self, control_nodes: Tuple4F, sample_nodes: Tuple4F, num_spline_nodes: int,
                 road_bbox: RoadBoundingBox):
        super().__init__()
        BeamNGMember.counter += 1
        self.name = f'Road{str(BeamNGMember.counter)}'
        self.name_ljust = self.name.ljust(7)
        self.control_nodes = control_nodes
        self.sample_nodes = sample_nodes
        self.num_spline_nodes = num_spline_nodes
        self.road_bbox = road_bbox
        self.config: BeamNGConfig = None
        self.problem: 'BeamNGProblem' = None
        self._evaluator: BeamNGEvaluator = None
        self.length = None



    def clone(self):
        res = BeamNGMember(list(self.control_nodes), list(self.sample_nodes), self.num_spline_nodes, self.road_bbox)
        res.config = self.config
        res.problem = self.problem
        res.distance_to_boundary = self.distance_to_boundary

        return res

    def to_dict(self) -> dict:
        return {
            'control_nodes': self.control_nodes,
            'sample_nodes': self.sample_nodes,
            'num_spline_nodes': self.num_spline_nodes,
            'road_bbox_size': self.road_bbox.bbox.bounds,
            'distance_to_boundary': self.distance_to_boundary
        }

    @classmethod
    def from_dict(cls, dict: Dict):
        road_bbox = RoadBoundingBox(dict['road_bbox_size'])
        res = BeamNGMember([tuple(t) for t in dict['control_nodes']],
                           [tuple(t) for t in dict['sample_nodes']],
                           dict['num_spline_nodes'], road_bbox)
        res.distance_to_boundary = dict['distance_to_boundary']
        return res

    def evaluate(self, executor):
        road_points = [(node[0], node[1]) for node in self.sample_nodes]
        #road_points = RoadGenerator(num_control_nodes=NODES, max_angle=MAX_ANGLE, seg_length=SEG_LENGTH,
#                                    num_spline_nodes=NUM_SPLINE_NODES).generate()
        the_test = RoadTestFactory.create_road_test(road_points)

        test_outcome, description, execution_data = executor.execute_test(the_test)

        if test_outcome == "INVALID":
            self.length = 10000
            min_oob_distance = 10000
        else:
            self.length = the_test.get_road_length()
            min_oob_distance = min(state.oob_distance for state in execution_data)

        self.distance_to_boundary = min_oob_distance
        log.info("Outcome %s", test_outcome)
        if test_outcome != "INVALID":
            log.info("Minimum oob_Distance %s", min_oob_distance)
            log.info("Length %s", self.length)

    def needs_evaluation(self):
        return self.distance_to_boundary is None

    def clear_evaluation(self):
        self.distance_to_boundary = None

    def is_valid(self):
        return (RoadPolygon.from_nodes(self.sample_nodes).is_valid() and
                self.road_bbox.contains(RoadPolygon.from_nodes(self.control_nodes[1:-1])))

    def distance(self, other: 'BeamNGMember'):
        return iterative_levenshtein(self.sample_nodes, other.sample_nodes)


    def to_tuple(self):
        import numpy as np
        barycenter = np.mean(self.control_nodes, axis=0)[:2]
        return barycenter

    def mutate(self) -> 'BeamNGMember':
        RoadMutator(self, lower_bound=-int(self.problem.config.MUTATION_EXTENT), upper_bound=int(self.problem.config.MUTATION_EXTENT)).mutate()
        self.distance_to_boundary = None
        return self

    def __repr__(self):
        eval_boundary = 'na'
        if self.distance_to_boundary:
            eval_boundary = str(self.distance_to_boundary)
            if self.distance_to_boundary > 0:
                eval_boundary = '+' + eval_boundary
            eval_boundary = '~' + eval_boundary
        eval_boundary = eval_boundary[:7].ljust(7)
        #h = hashlib.sha256(str([tuple(node) for node in self.control_nodes]).encode('UTF-8')).hexdigest()[-5:]
        return f'{self.name_ljust}'


class RoadMutator:
    NUM_UNDO_ATTEMPTS = 20

    def __init__(self, road: BeamNGMember, lower_bound=-2, upper_bound=2):
        self.road = road
        self.lower_bound = lower_bound
        self.higher_bound = upper_bound

    def mutate_gene(self, index, xy_prob=0.5) -> Tuple[int, int]:
        gene = list(self.road.control_nodes[index])
        # Choose the mutation extent
        mut_value = random.randint(self.lower_bound, self.higher_bound)
        # Avoid to choose 0
        if mut_value == 0:
            mut_value += 1
        c = 0
        if random.random() < xy_prob:
            c = 1
        gene[c] += mut_value
        self.road.control_nodes[index] = tuple(gene)
        self.road.sample_nodes = catmull_rom(self.road.control_nodes, self.road.num_spline_nodes)
        return c, mut_value

    def undo_mutation(self, index, c, mut_value):
        gene = list(self.road.control_nodes[index])
        gene[c] -= mut_value
        self.road.control_nodes[index] = tuple(gene)
        self.road.sample_nodes = catmull_rom(self.road.control_nodes, self.road.num_spline_nodes)

    def mutate(self, num_undo_attempts=10):
        backup_nodes = list(self.road.control_nodes)
        attempted_genes = set()
        n = len(self.road.control_nodes) - 2

        def next_gene_index() -> int:
            if len(attempted_genes) == n:
                return -1
            i = random.randint(3, n-3)
            while i in attempted_genes:
                i = random.randint(3, n-3)
            attempted_genes.add(i)
            assert 3 <= i <= n-3
            return i

        gene_index = next_gene_index()

        while gene_index != -1:
            c, mut_value = self.mutate_gene(gene_index)

            attempt = 0

            is_valid = self.road.is_valid()
            while not is_valid and attempt < num_undo_attempts:
                self.undo_mutation(gene_index, c, mut_value)
                c, mut_value = self.mutate_gene(gene_index)
                attempt += 1
                is_valid = self.road.is_valid()

            if is_valid:
                break
            else:
                gene_index = next_gene_index()

        if gene_index == -1:
            raise ValueError("No gene can be mutated")

        assert self.road.is_valid()
        assert self.road.control_nodes != backup_nodes