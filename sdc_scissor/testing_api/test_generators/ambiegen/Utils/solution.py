from sdc_scissor.testing_api.test_generators.ambiegen.Utils.vehicle import Car
import sdc_scissor.testing_api.test_generators.ambiegen.config as cf
from sdc_scissor.testing_api.test_generators.ambiegen.Utils.car_road import Map

# from code_pipeline.beamng_executor import BeamngExecutor
# from code_pipeline.tests_generation import RoadTestFactory


class Solution:

    """
    This is a class to represent one individual of the genetic algorithm
    """

    def __init__(self):

        self.road_points = []
        self.states = {}
        self.car = Car(cf.model["speed"], cf.model["steer_ang"], cf.model["map_size"])
        self.road_builder = Map(cf.model["map_size"])
        self.fitness = 0
        self.car_path = []
        self.novelty = 0
        self.intp_points = []
        self.too_sharp = 0
        self.just_fitness = 0

    def eval_fitness(self):
        road = self.road_points
        if not road:  # if no road points were calculated yet
            self.get_points()
            self.remove_invalid_cases()
            road = self.road_points

        if len(self.road_points) <= 2:
            self.fitness = 0
        else:
            self.intp_points = self.car.interpolate_road(road)
            self.fitness, self.car_path = self.car.execute_road(self.intp_points)

        return

    # def car_model_fit(self):

    # the_executor = BeamngExecutor(cf.model["map_size"])

    # the_test = RoadTestFactory.create_road_test(self.road_points)

    # fit = the_executor._eval_tc(the_test)

    # return fit

    def get_points(self):
        self.road_points = self.road_builder.get_points_from_states(self.states)

    def remove_invalid_cases(self):
        self.states, self.road_points = self.road_builder.remove_invalid_cases(self.road_points, self.states)

    def calc_novelty(self, old, new):
        novelty = 0
        difference = abs(len(new) - len(old)) / 2
        novelty += difference
        if len(new) <= len(old):
            shorter = new
        else:
            shorter = old
        for tc in shorter:
            if old[tc]["state"] == new[tc]["state"]:
                value_list = [old[tc]["value"], new[tc]["value"]]
                ratio = max(value_list) / min(value_list)
                if ratio >= 2:
                    novelty += 0.5
            else:
                novelty += 1
        return -novelty

    @property
    def n_states(self):
        return len(self.states)
