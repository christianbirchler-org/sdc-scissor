import numpy as np
import logging as log
import random
from time import sleep

from sdc_scissor.testing_api.test_generators.frenetic.src.generators.base_frenet_generator import BaseFrenetGenerator


class CustomFrenetGenerator(BaseFrenetGenerator):
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
        count=None,
    ):
        self.count = count
        # Spending 20% of the time on random generation
        # Set this value to 1.0 to generate fully random results.
        self.random_gen_budget = random_budget
        # Margin size w.r.t the map
        self.margin = 10
        # Storing the ancestors of a test that failed to reduce close relatives.
        self.ancestors_of_failed_tests = set()
        self.kill_ancestors = kill_ancestors
        # Only considering tests with a min_oob_distance < threshold for mutation
        # define min_oobd_threshold = 2.0 to remove this feature
        # TODO: Consider updating this value after the initial population
        # df[df.outcome != 'INVALID'].min_oob_distance.quantile(0.25)
        self.min_oobd_threshold = -0.5
        # Set crossover frequency to 0 for no crossover
        self.crossover_candidates = crossover_candidates
        self.crossover_frequency = crossover_frequency

        # Fix number or fix distance policy
        self.max_length = 30
        self.min_step_size = 7
        if map_size < 150:
            # Fix Points
            self.number_of_points = 15
            self.frenet_step = max(self.min_step_size, map_size // self.number_of_points)
        else:
            # Fix Distance
            # Number of generated kappa points depends on the size of the map + random variation
            self.frenet_step = 10
            self.number_of_points = min(map_size // self.frenet_step, self.max_length)

        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, strict_father=strict_father)

    def start(self):
        log.info("Test generation frenetic.")
        return self.generate_initial_population()
        # self.generate_mutants()
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
            road_points = self.execute_frenet_test(kappas, frenet_step=self.frenet_step)
            road_points_collection.append(road_points)
            # print(road_points)
        return road_points_collection

    def generate_mutants(self):
        # Iterating the tests according to the value of the min_oob_distance (closer to fail).
        self.recent_count = 0
        while self.executor.get_remaining_time() > 0:
            if 0.0 in set(self.df["visited"]) or 1.0 in set(self.df["visited"]):
                # TODO: The values are become float if there is a nan due to ERROR.
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
                self.execute_frenet_test(kappas, frenet_step=self.frenet_step)
            if 0 < self.crossover_frequency <= self.recent_count:
                log.info("Entering crossover phase.")
                self.crossover()
                self.recent_count = 0

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
            ("increase all kappas 10~20%", self.increase_kappas),
            ("randomly modify 1 to 5 kappas", self.random_modification),
        ]

        self.perform_kappa_mutations(kappa_mutations, parent, parent_info)

    def mutate_failed_test(self, parent, parent_info):
        # Only reversing roads that produced a failure already
        # Mutations to the road
        # TODO: Obtain the kappa values given the cartesians.
        road_points = parent.road.item()
        # Execute reversed original test
        log.info("Mutation function: {:s}".format("reverse road"))
        log.info(
            "Parent ({:s}) {:0.3f} accum_neg_oob and {:0.3f} min oob distance".format(
                parent.outcome.item(), parent.accum_neg_oob.item(), parent.min_oob_distance.item()
            )
        )
        # Do not revisit a reverse road
        self.execute_test(
            road_points[::-1], method="reversed road", extra_info={"visited": True}, parent_info=parent_info
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
            while self.executor.get_remaining_time() > 0 and kids_count < len(candidates):
                his_id, her_id = random.sample(list(candidates.index), 2)
                father = self.df.iloc[his_id]["kappas"]
                mother = self.df.iloc[her_id]["kappas"]
                if random.random() < 0.5:
                    kids = self.chromosome_crossover(father, mother)
                    name = "chromosome crossover"
                else:
                    kids = self.single_point_crossover(father, mother)
                    name = "single point crossover"
                while self.executor.get_remaining_time() > 0 and len(kids) > 0:
                    kappas = kids.pop()
                    kids_count += 1
                    self.execute_frenet_test(
                        kappas, method=name, frenet_step=self.frenet_step, parent_info={}, extra_info={}
                    )

    @staticmethod
    def chromosome_crossover(him, her):
        """
        him: list of kappas
        her: list of kappas
        returns: a list of kappas of the length of the shortest list
        """
        son = []
        for i in range(min(len(him), len(her))):
            if random.random() < 0.5:
                son.append(him[i])
            else:
                son.append(her[i])
        return [son]

    @staticmethod
    def single_point_crossover(him, her):
        """
        him: list of kappas
        her: list of kappas
        returns: Two lists of kappas
        """
        son = him[len(him) // 2 :] + her[: len(her) // 2]
        daughter = her[len(her) // 2 :] + him[: len(him) // 2]
        return [son, daughter]

    def perform_kappa_mutations(self, kappa_mutations, parent, parent_info, extra_info={}):
        # Only considering paths with more than 10 kappa points for mutations
        # kappas might be empty if the parent was obtained from reverse road points mutation
        kappas = parent.kappas.item()
        if kappas and len(kappas) > 10:
            i = 0
            while self.executor.get_remaining_time() > 0 and i < len(kappa_mutations):
                name, function = kappa_mutations[i]
                log.info("Generating mutants. Remaining time %s", self.executor.get_remaining_time())
                log.info("Mutation function: {:s}".format(name))
                log.info(
                    "Parent ({:s}) {:0.3f} accum_neg_oob and {:0.3f} min oob distance".format(
                        parent.outcome.item(), parent.accum_neg_oob.item(), parent.min_oob_distance.item()
                    )
                )
                m_kappas = function(kappas)
                outcome, _ = self.execute_frenet_test(
                    m_kappas, frenet_step=self.frenet_step, method=name, parent_info=parent_info, extra_info=extra_info
                )

                # When there is a mutant of this branch that fails, we stop mutating this branch.
                if outcome == "FAIL" and self.kill_ancestors > 0:
                    for ancestor_id in parent_info["ancestors"][-self.kill_ancestors :]:
                        self.ancestors_of_failed_tests.add(ancestor_id)
                    break
                i += 1

    @staticmethod
    def get_next_kappa(last_kappa, kappa_bound=0.05, kappa_delta=0.07):
        return random.choice(
            np.linspace(max(-kappa_bound, last_kappa - kappa_delta), min(kappa_bound, last_kappa + kappa_delta))
        )

    @staticmethod
    def increase_kappas(kappas):
        m = 1.1 + 0.1 * random.random()
        return list(map(lambda x: x * m, kappas))

    @staticmethod
    def add_kappas(kappas):
        # number of kappas to added
        k = random.randint(1, 5)
        modified_kappas = kappas[:]
        last_kappa = kappas[-1]
        while k > 0:
            # Randomly add a kappa
            modified_kappas.append(CustomFrenetGenerator.get_next_kappa(last_kappa))
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

    @staticmethod
    def random_modification(kappas):
        # number of kappas to be modified
        k = random.randint(1, 5)
        # Randomly modified kappa
        indexes = random.sample(range(len(kappas) - 1), k)
        modified_kappas = kappas[:]
        for i in indexes:
            modified_kappas[i] += random.choice(np.linspace(-0.05, 0.05))
        return modified_kappas

    def generate_random_test(self, kappa_delta=0.05, kappa_bound=0.07):
        """Generates a test using frenet framework to determine the curvature of the points.
         Currently using an initial setup similar to the GUI.
         TODO: Make the frenet setup part of the experiment to adapt w.r.t. the output of the tests.
        Args:
            frenet_step: The distance between to points.
            theta0: The initial angle of the line. (1.57 == 90 degrees)
            kappa_delta: The maximum difference between two consecutive kappa values.
            kappa_bound: The maximum value of kappa allowed.
        Returns:
            a list of kappa values and its cartesian representation.
        """
        points = self.number_of_points + random.randint(-5, 5)
        # Producing randomly generated kappas for the given setting.
        kappas = [0.0] * points
        for i in range(len(kappas)):
            kappas[i] = CustomFrenetGenerator.get_next_kappa(kappas[i - 1], kappa_bound, kappa_delta)

        return kappas


class Frenetic(CustomFrenetGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None):
        super().__init__(
            time_budget=time_budget,
            executor=executor,
            map_size=map_size,
            kill_ancestors=0,
            strict_father=False,
            random_budget=3600,
            crossover_candidates=20,
            crossover_frequency=40,
        )
