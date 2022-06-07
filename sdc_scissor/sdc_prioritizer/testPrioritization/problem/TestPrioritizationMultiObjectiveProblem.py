from pymoo.core.problem import Problem
import multiprocessing as mp


def ff_eval(x):
    global costs
    global distances
    f1 = 0.0
    f2 = 0.0

    for index, test_id in enumerate(x[:-1]):
        f1 += costs[test_id] / (index + 1)
        f2 -= distances[test_id][x[index + 1]] / (index + 1)
    return f1, f2


class TestPrioritizationMultiObjectiveProblem(Problem):
    generation_counter = 0

    def __init__(self, genome_length, distancesp, costsp):

        super().__init__(n_var=genome_length, n_obj=2, n_constr=0, xl=0.0, xu=genome_length)
        global costs
        costs = costsp
        global distances
        distances = distancesp

    def _evaluate(self, x, out, *args, **kwargs):

        pool1 = mp.Pool(processes=5)

        new_rows2 = pool1.map(ff_eval, x)
        pool1.terminate()
        out["F"] = new_rows2
