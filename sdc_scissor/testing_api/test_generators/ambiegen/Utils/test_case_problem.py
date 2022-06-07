from pymoo.model.problem import Problem


class TestCaseProblem(Problem):
    """
    Module to calculate the fitnes of the individuals
    """

    def __init__(self):
        super().__init__(n_var=1, n_obj=2, n_constr=1, elementwise_evaluation=True)

    def _evaluate(self, x, out, *args, **kwargs):
        s = x[0]
        s.get_points()  # transform the states into actual points (mutation and crossover operations are performed on states)
        s.remove_invalid_cases()
        s.eval_fitness()
        out["F"] = [s.fitness, s.novelty]
        out["G"] = 4 - s.fitness * (-1)
