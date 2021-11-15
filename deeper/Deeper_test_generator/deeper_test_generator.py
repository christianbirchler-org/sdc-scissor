import numpy

from deap import base
from deap import creator
from deap import tools

from deeper.Deeper_test_generator.archive_impl import GreedyArchive
from deeper.Deeper_test_generator.log_setup import get_logger
from deeper.Deeper_test_generator.beamng_problem import BeamNGProblem
from deeper.Deeper_test_generator.beamng_config import BeamNGConfig

log = get_logger(__file__)


class DeeperTestGenerator():
    """
        Generates a single test to show how to control the shape of the road by controlling the positio of the
        road points. We assume a map of 200x200
    """

    def __init__(self, time_budget=None, executor=None, map_size=None):
        self.time_budget = time_budget
        self.executor = executor
        self.map_size = map_size

    def start(self):
        # start = time.monotonic()
        log.info("Test Generation Started by Deeper")
        config = BeamNGConfig()
        # problem = BeamNGProblem(self.executor, config, GreedyArchive(config.ARCHIVE_THRESHOLD))
        problem = BeamNGProblem(self.executor, config, GreedyArchive())
        # random.seed()

        creator.create("FitnessMulti", base.Fitness, weights=config.fitness_weights)
        creator.create("Individual", problem.deap_individual_class(), fitness=creator.FitnessMulti)

        toolbox = base.Toolbox()
        problem.toolbox = toolbox

        toolbox.register("individual", problem.deap_generate_individual)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", problem.deap_evaluate_individual)
        toolbox.register("mutate", problem.deap_mutate_individual)
        toolbox.register("select", tools.selNSGA2)

        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", numpy.min, axis=0)
        stats.register("max", numpy.max, axis=0)
        stats.register("avg", numpy.mean, axis=0)
        stats.register("std", numpy.std, axis=0)
        logbook = tools.Logbook()
        logbook.header = "gen", "evals", "min", "max", "avg", "std"

        # Generate initial population.
        log.info("Starting Generating Initial Test Roads ")
        pop = toolbox.population(n=config.POPSIZE)

        # #**********************************************************************
        # if time.monotonic() > start + self.time_budget:
        #     log.warning("Time budget is over, cannot run more tests. FORCE EXIT ")
        #     raise TimeoutError("Sorry, Out of time")
        # #**********************************************************************

        # Evaluate the initial population.
        # Note: the fitness functions are all invalid before the first iteration since they have not been evaluated.
        invalid_ind = [ind for ind in pop if not ind.fitness.valid]

        # # **********************************************************************
        # if time.monotonic() > start + self.time_budget:
        #     log.warning("Time budget is over, cannot run more tests. FORCE EXIT")
        #     raise TimeoutError("Sorry, Out of time")
        # # **********************************************************************

        # problem.pre_evaluate_members(invalid_ind)

        # # **********************************************************************
        # if time.monotonic() > start + self.time_budget:
        #     log.warning("Time budget is over, cannot run more tests. FORCE EXIT")
        #     raise TimeoutError("Sorry, Out of time")
        # # **********************************************************************

        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # # **********************************************************************
        # if time.monotonic() > start + self.time_budget:
        #     log.warning("Time budget is over, cannot run more tests. FORCE EXIT")
        #     raise TimeoutError("Sorry, Out of time")
        # # **********************************************************************

        problem.archive.process_population(pop)

        pop = toolbox.select(pop, len(pop))

        # record = stats.compile(pop)
        # logbook.record(gen=0, evals=len(invalid_ind), **record)
        # print(logbook.stream)

        # # **********************************************************************
        # if time.monotonic() > start + self.time_budget:
        #     log.warning("Time budget is over, cannot run more tests. FORCE EXIT")
        #     raise TimeoutError("Sorry, Out of time")
        # # **********************************************************************

        problem.on_iteration(0, pop)

        for gen in range(1, config.NUM_GENERATIONS):

            log.info("Selection Started ")
            offspring = tools.selTournamentDCD(pop, len(pop))

            # # **********************************************************************
            # if time.monotonic() > start + self.time_budget:
            #     log.warning("Time budget is over, cannot run more tests. FORCE EXIT")
            #     raise TimeoutError("Sorry, Out of time")
            # # **********************************************************************

            offspring = [ind.clone() for ind in offspring]

            # # **********************************************************************
            # if time.monotonic() > start + self.time_budget:
            #     log.warning("Time budget is over, cannot run more tests. FORCE EXIT")
            #     raise TimeoutError("Sorry, Out of time")
            # # **********************************************************************

            problem.reseed(pop)

            # # **********************************************************************
            # if time.monotonic() > start + self.time_budget:
            #     log.warning("Time budget is over, cannot run more tests. FORCE EXIT")
            #     raise TimeoutError("Sorry, Out of time")
            # # **********************************************************************

            log.info("Mutation Started ")
            for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
                toolbox.mutate(ind1)
                toolbox.mutate(ind2)
                del ind1.fitness.values, ind2.fitness.values

            # # **********************************************************************
            # if time.monotonic() > start + self.time_budget:
            #     log.warning("Time budget is over, cannot run more tests. FORCE EXIT")
            #     raise TimeoutError("Sorry, Out of time")
            # # **********************************************************************

            # Evaluate the individuals with an invalid fitness
            to_eval = offspring + pop
            invalid_ind = list(to_eval)

            # problem.pre_evaluate_members(invalid_ind)

            # # **********************************************************************
            # if time.monotonic() > start + self.time_budget:
            #     log.warning("Time budget is over, cannot run more tests. FORCE EXIT")
            #     raise TimeoutError("Sorry, Out of time")
            # # **********************************************************************

            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            problem.archive.process_population(offspring + pop)

            # # **********************************************************************
            # if time.monotonic() > start + self.time_budget:
            #     log.warning("Time budget is over, cannot run more tests. FORCE EXIT")
            #     raise TimeoutError("Sorry, Out of time")
            # # **********************************************************************

            # Select the next generation population
            pop = toolbox.select(pop + offspring, config.POPSIZE)
            record = stats.compile(pop)
            logbook.record(gen=gen, evals=len(invalid_ind), **record)
            # print(logbook.stream)
            problem.on_iteration(gen, pop)
        return pop, logbook
