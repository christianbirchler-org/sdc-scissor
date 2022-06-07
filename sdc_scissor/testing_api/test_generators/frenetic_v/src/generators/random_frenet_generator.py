import numpy as np
import logging as log
import random
from time import sleep

from sdc_scissor.testing_api.test_generators.frenetic_v.src.generators.base_frenet_generator import BaseFrenetVGenerator


class CustomFrenetVGenerator(BaseFrenetVGenerator):
    """
    Generates tests using the frenet framework to determine curvatures.
    """

    def __init__(
        self,
        time_budget=None,
        executor=None,
        map_size=None,
        kill_ancestors=1,
        strict_father=True,
        random_budget=3600,
        crossover_candidates=20,
        crossover_frequency=0,
        normalize=False,
        global_bound=0.06232,
        local_bound=0.05,
        max_number_of_points=30,
        min_number_of_points=10,
        segment_length=10,
        min_oob_distance_threshold=-0.5,
        store_additional_data=False,
        count=None,
    ):

        self.count = count
        # Time spent on initial random generation
        self.random_gen_budget = random_budget
        # Margin size w.r.t the map
        self.margin = 10
        # Storing the ancestors of a test that failed to reduce close relatives.
        self.ancestors_of_failed_tests = set()
        self.kill_ancestors = kill_ancestors
        # Only considering tests with a min_oob_distance < threshold for mutation
        # define min_oobd_threshold = 2.0 to remove this feature
        self.min_oobd_threshold = min_oob_distance_threshold
        # Set crossover frequency to 0 for no crossover
        self.crossover_candidates = crossover_candidates
        self.crossover_frequency = crossover_frequency

        self.normalize = normalize
        self.global_bound = global_bound
        self.local_bound = local_bound

        # Global bounds on the number of values
        self.min_number_of_points = min_number_of_points
        self.max_number_of_points = max_number_of_points

        # Fix Distance
        # Number of generated kappa points depends on the size of the map + random variation
        self.number_of_points = min(int(map_size // segment_length), self.max_number_of_points)

        super().__init__(
            executor=executor,
            map_size=map_size,
            strict_father=strict_father,
            segment_length=segment_length,
            store_additional_data=store_additional_data,
        )

    def start(self):
        log.info("Test generation freneticV.")
        return self.generate_initial_population()
        # self.generate_mutants()
        # self.store_dataframe()
        # sleep(10)

    def generate_initial_population(self):
        # while self.executor.get_remaining_time() > (self.time_budget - self.random_gen_budget):
        road_points_collection = []
        cnt = 0
        while cnt < self.count:
            # print(cnt)
            cnt += 1
            log.info("Random generation. Remaining time %s", 10)
            kappas = self.generate_random_test()
            road_points = self.execute_frenet_test(kappas)
            road_points_collection.append(road_points)
            # print(road_points)
        return road_points_collection

    def generate_mutants(self):
        # Iterating the tests according to the value of the min_oob_distance (closer to fail).
        self.recent_count = 0
        while not self.executor.is_over():
            if 0.0 in set(self.df["visited"]) or 1.0 in set(self.df["visited"]):
                # TODO: The values are becoming float if there is a nan value due to ERROR from the simulator.
                log.info("Converting visited column to boolean...")
                self.df["visited"] = self.df["visited"].map(lambda x: True if x == 1.0 else False)
            parent = (
                self.df[
                    ((self.df.outcome == "PASS") | (self.df.outcome == "FAIL"))
                    & (~self.df.visited)
                    & (self.df.min_oob_distance < self.min_oobd_threshold)
                ]
                .sort_values("min_oob_distance", ascending=True)
                .head(1)
            )
            if len(parent):
                self.df.at[parent.index, "visited"] = True
                self.mutate_test(parent)
            else:
                # If there is no good parent try random generation
                log.info("There is no good candidate for mutation.")
                kappas = self.generate_random_test()
                self.execute_frenet_test(kappas)
            if 0 < self.crossover_frequency <= self.recent_count:
                log.info("Entering crossover phase.")
                self.crossover()
                self.recent_count = 0

    def normalize_test(self, test):
        test[0] = max(min(test[0], self.global_bound), -self.global_bound)
        for i in range(1, len(test)):
            previous = test[i - 1]
            min_bound = max(-self.global_bound, previous - self.local_bound)
            max_bound = min(self.global_bound, previous + self.local_bound)
            test[i] = max(min(test[i], max_bound), min_bound)
        return test

    def execute_frenet_test(self, kappas, method="random", parent_info={}, extra_info={}):
        if self.normalize:
            kappas = self.normalize_test(kappas)
        return super().execute_frenet_test(kappas, method, parent_info, extra_info)

    def mutate_test(self, parent):
        # Parent info to be added to the dataframe
        ancestors = []
        if parent.method.item() != "random":
            ancestors = parent.ancestors.item()
        ancestors += [parent.index.item()]

        parent_info = {
            "parent_index": parent.index.item(),
            "parent_outcome": parent.outcome.item(),
            "parent_min_oob_distance": parent.min_oob_distance.item(),
            "generation": parent.generation.item() + 1,
            "ancestors": ancestors,
        }
        if self.kill_ancestors > 0:
            # Looking to close relatives to avoid too similar tests
            for ancestor_id in ancestors[-self.kill_ancestors :]:
                if ancestor_id in self.ancestors_of_failed_tests:
                    return
        # Applying different mutations depending on the outcome
        if parent.outcome.item() == "FAIL":
            self.mutate_failed_test(parent, parent_info)
        else:
            self.mutate_passed_test(parent, parent_info)

    def mutate_passed_test(self, parent, parent_info):
        kappa_mutations = [
            ("add 1 to 5 kappas at the end", self.add_kappas),
            ("randomly remove 1 to 5 kappas", self.randomly_remove_kappas),
            ("remove 1 to 5 kappas from front", lambda ks: ks[random.randint(1, 5) :]),
            ("remove 1 to 5 kappas from tail", lambda ks: ks[: -random.randint(1, 5)]),
            ("increase all kappas 1~5%", self.increase_kappas),
            ("randomly modify 1 to 5 kappas", self.random_modification),
        ]

        self.perform_kappa_mutations(kappa_mutations, parent, parent_info)

    def mutate_failed_test(self, parent, parent_info):
        # Only reversing roads that produced a failure already
        log.info(
            "Parent ({:s}) {:0.3f} accum_neg_oob and {:0.3f} min oob distance".format(
                parent.outcome.item(), parent.accum_neg_oob.item(), parent.min_oob_distance.item()
            )
        )

        # mutations that we may want to avoid in tests that passed because they are easily reversible
        kappa_mutations = [
            ("reverse kappas", lambda ks: ks[::-1]),
            ("split and swap kappas", lambda ks: ks[int(len(ks) / 2) :] + ks[: int(len(ks) / 2)]),
            ("flip sign kappas", lambda ks: list(map(lambda x: x * -1.0, ks))),
        ]

        self.perform_kappa_mutations(kappa_mutations, parent, parent_info, extra_info={"visited": True})

    def crossover(self):
        # TODO: Add parent information
        candidates = (
            self.df[
                ((self.df.outcome == "PASS") | (self.df.outcome == "FAIL"))
                & (~self.df.kappas.isna())
                & (self.df.min_oob_distance < self.min_oobd_threshold)
            ]
            .sort_values("min_oob_distance", ascending=True)
            .head(self.crossover_candidates)
        )

        if len(candidates) > 4:
            kids_count = 0
            while not self.executor.is_over() and kids_count < len(candidates):
                his_id, her_id = random.sample(list(candidates.index), 2)
                father = self.df.iloc[his_id]["kappas"]
                mother = self.df.iloc[her_id]["kappas"]
                if random.random() < 0.5:
                    kids = self.chromosome_crossover(father, mother)
                    name = "chromosome crossover"
                else:
                    kids = self.single_point_crossover(father, mother)
                    name = "single point crossover"
                while not self.executor.is_over() and len(kids) > 0:
                    kappas = kids.pop()
                    kids_count += 1
                    self.execute_frenet_test(kappas, method=name, parent_info={}, extra_info={})

    @staticmethod
    def chromosome_crossover(parent_1, parent_2):
        """

        :param parent_1: list of kappas
        :param parent_2: list of kappas
        :return: a list of kappas of the length of the shortest list
        """
        child = []
        for i in range(min(len(parent_1), len(parent_2))):
            if random.random() < 0.5:
                child.append(parent_1[i])
            else:
                child.append(parent_2[i])
        return [child]

    @staticmethod
    def single_point_crossover(parent_1, parent_2):
        """

        :param parent_1: list of test
        :param parent_2: list of test
        :return: Two lists of test
        """

        # more or less in the middle
        amount = min(len(parent_1) // 2 - 2, len(parent_2) // 2 - 2)
        variability = random.randint(-amount, amount)
        parent_1_split_point = len(parent_1) // 2 + variability
        parent_2_split_point = len(parent_2) // 2 + variability

        child_1 = parent_1[parent_1_split_point:] + parent_2[:parent_2_split_point]
        child_2 = parent_2[parent_2_split_point:] + parent_1[:parent_1_split_point]
        return [child_1, child_2]

    def get_remaining_time(self):
        return self.executor.time_budget.get_remaining_real_time()

    def perform_kappa_mutations(self, kappa_mutations, parent, parent_info, extra_info={}):
        # Only considering paths with more than 10 kappa points for mutations
        # kappas might be empty if the parent was obtained from reverse road points mutation
        kappas = parent.kappas.item()
        if kappas and len(kappas) > self.min_number_of_points:
            i = 0
            while not self.executor.is_over() and i < len(kappa_mutations):
                name, function = kappa_mutations[i]
                log.info("Generating mutants. Remaining time %s", self.get_remaining_time())
                log.info("Mutation function: {:s}".format(name))
                log.info(
                    "Parent ({:s}) {:0.3f} accum_neg_oob and {:0.3f} min oob distance".format(
                        parent.outcome.item(), parent.accum_neg_oob.item(), parent.min_oob_distance.item()
                    )
                )
                m_kappas = function(kappas)
                outcome, _ = self.execute_frenet_test(
                    m_kappas, method=name, parent_info=parent_info, extra_info=extra_info
                )

                # When there is a mutant of this branch that fails, we stop mutating this branch.
                if outcome == "FAIL" and self.kill_ancestors > 0:
                    for ancestor_id in parent_info["ancestors"][-self.kill_ancestors :]:
                        self.ancestors_of_failed_tests.add(ancestor_id)
                    break
                i += 1

    def get_next_kappa(self, last_kappa):
        return random.choice(
            np.linspace(
                max(-self.global_bound, last_kappa - self.local_bound),
                min(self.global_bound, last_kappa + self.local_bound),
            )
        )

    @staticmethod
    def increase_kappas(kappas):
        m = 1.01 + 0.04 * random.random()
        return list(map(lambda x: x * m, kappas))

    def add_kappas(self, kappas):
        # number of kappas to added
        k = random.randint(1, 5)
        modified_kappas = kappas[:]
        last_kappa = kappas[-1]
        while k > 0:
            # Randomly add a kappa
            modified_kappas.append(self.get_next_kappa(last_kappa))
            k -= 1
        return modified_kappas

    @staticmethod
    def randomly_remove_kappas(kappas):
        # number of kappas to be removed
        k = random.randint(1, 5)
        modified_kappas = kappas[:]
        while k > 0 and len(modified_kappas) > 5:
            # Randomly remove a kappa
            i = random.randint(0, len(modified_kappas) - 1)
            del modified_kappas[i]
            k -= 1
        return modified_kappas

    def random_modification(self, kappas):
        # number of kappas to be modified
        k = random.randint(1, 5)
        # Randomly modified kappa
        indexes = random.sample(range(len(kappas) - 1), k)
        modified_kappas = kappas[:]
        for i in indexes:
            modified_kappas[i] += random.choice(np.linspace(-self.global_bound, self.global_bound))
        return modified_kappas

    def generate_random_test(self):
        """
        Generates a test using frenet framework to determine the curvature of the points.

        :return: a list of kappa values and its cartesian representation.
        """
        points = self.number_of_points + random.randint(-5, 5)
        # Producing randomly generated kappas for the given setting.
        kappas = [0.0] * points
        for i in range(len(kappas)):
            kappas[i] = self.get_next_kappa(kappas[i - 1])

        return kappas


class FreneticV(CustomFrenetVGenerator):
    def __init__(self, executor=None, map_size=None):
        super().__init__(
            executor=executor,
            map_size=map_size,
            kill_ancestors=0,
            strict_father=False,
            random_budget=3600,
            crossover_candidates=20,
            crossover_frequency=40,
            normalize=True,
            global_bound=0.06712,
            local_bound=0.04812,
            segment_length=5,
            max_number_of_points=50,
            min_number_of_points=20,
        )
