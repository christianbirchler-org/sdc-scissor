from typing import List

import numpy as np
from deeper.Deeper_test_generator.individual import Individual
from deeper.Deeper_test_generator.member import Member


def get_radius_seed(solution: List[Individual]):
    # Calculate the distance between each misclassified digit and the seed (mindist metric)
    if len(solution) == 0:
        return None
    distances = list()
    for i in solution:
        oob_input = i.members_by_sign()[0]
        dist = oob_input.distance(i.seed)
        distances.append(dist)
    radius = np.mean(distances)
    return radius


def get_diameter(solution: List[Member]):
    # Calculate the distance between each misclassified digit and the farthest element of the solution (diameter metric)
    if len(solution) == 0:
        return None
    max_distances = list()
    for i1 in solution:
        maxdist = float(0)
        for i2 in solution:
            if i1 != i2:
                dist = i1.distance(i2)
                if dist > maxdist:
                    maxdist = dist
        max_distances.append(maxdist)
    diameter = np.mean(max_distances)
    return diameter
