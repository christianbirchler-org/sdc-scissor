import numpy as np
import random


from pymoo.core.mutation import Mutation


class HybridMut(Mutation):
    def __init__(self, prob=1.0):
        super().__init__()
        self.prob = prob

    def _do(self, problem, X, **kwargs):
        X = X[: int(len(X) / 2)]
        Y = X.copy()

        for child in Y:
            mutation_points = []
            while len(mutation_points) < 2:
                temp_point = random.randint(0, len(child) - 1)
                if temp_point not in mutation_points:
                    mutation_points.append(temp_point)
            mutation_selector_prob = random.uniform(0, 1)
            if mutation_selector_prob <= 0.33:

                temp = child[mutation_points[0]]
                child[mutation_points[0]] = child[mutation_points[1]]
                child[mutation_points[1]] = temp

            elif mutation_selector_prob <= 0.66:

                min_index = min(mutation_points)
                max_index = max(mutation_points)

                child[min_index : max_index + 1] = np.array(list(reversed(child[min_index : max_index + 1])))

            else:

                temp = child[mutation_points[0]]
                child = np.delete(child, mutation_points[0])
                child = np.insert(child, mutation_points[1], temp)

        return Y
