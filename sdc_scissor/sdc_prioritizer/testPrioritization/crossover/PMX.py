from pymoo.core.crossover import Crossover
import numpy as np
import random


def pmx(parent1, parent2):
    cutPoint = random.randint(0, len(parent1) - 1)
    head = parent1[:cutPoint]
    tail = []
    for test_id in parent2:
        if test_id not in head:
            tail.append(test_id)
    tail = np.array(tail)

    offspring = np.concatenate((head, tail), axis=None)

    return offspring


class PMXCrossover(Crossover):
    def __init__(self, **kwargs):
        super().__init__(2, 1, **kwargs)

    def _do(self, problem, X, **kwargs):
        _, n_matings, n_var = X.shape
        Y = np.full((self.n_offsprings, n_matings, n_var), -1, dtype=int)

        for i in range(n_matings):
            a, b = X[:, i, :]
            Y[0, i, :] = pmx(a, b)

        return Y
