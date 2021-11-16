import os
import shutil
from pathlib import Path
from time import sleep
from typing import Callable, List, Tuple, TypeVar
from typing import Union, Set

import numpy as np

from deeper.Deeper_test_generator.individual import Individual

T = TypeVar('T')


def delete_folder_recursively(path: Union[str, Path]):
    path = str(path)
    if not os.path.exists(path):
        return
    assert os.path.isdir(path), path
    print(f'Removing [{path}]')
    shutil.rmtree(path, ignore_errors=True)

    # sometimes rmtree fails to remove files
    for _tries in range(20):
        if os.path.exists(path):
            sleep(0.1)
            shutil.rmtree(path, ignore_errors=True)

    if os.path.exists(path):
        shutil.rmtree(path)

    if os.path.exists(path):
        raise Exception(f'Unable to remove folder [{path}]')


def evaluate_sparseness(ind: Individual, pop: Set[Individual]):
    elements = pop - {ind}
    if len(elements) == 0:
        return 1.0

    closest_element_dist = closest_elements(elements, ind, lambda a, b: a.distance(b))[0]
    return closest_element_dist[1]


def closest_indexes(array: List[T], element: T, distance_fun: Callable[[T, T], float]):
    indexes = list(np.argsort([distance_fun(element, el) for el in array]))
    return indexes


def closest_elements(elements_set: Set[T], obj: T, distance_fun: Callable[[T, T], float]) \
        -> List[Tuple[T, float]]:
    elements = list(elements_set)
    distances = [distance_fun(obj, el) for el in elements]
    indexes = list(np.argsort(distances))
    result = [(elements[idx], distances[idx]) for idx in indexes]
    return result


if __name__ == '__main__':
    import unittest

    class TestUtils(unittest.TestCase):
        def test_closest_indexes(self):
            def dist(a, b):
                return np.abs(a - b)

            target = closest_indexes([-30, 40, 1, -1], 0.1, dist)
            expected = [2, 3, 0, 1]

            self.assertEqual(target, expected)

        def test_closest_elements(self):
            def dist(a, b):
                return np.abs(a - b)

            target = closest_elements({-30, 40, 2, -2}, 1, dist)
            expected = [(2, 1), (-2, 3), (-30, 31), (40, 39)]

            self.assertEqual(target, expected)

    unittest.main()
