import numpy as np
from pymoo.model.sampling import Sampling
from sdc_scissor.testing_api.test_generators.ambiegen.Utils.solution import Solution

import sdc_scissor.testing_api.test_generators.ambiegen.config as cf
from sdc_scissor.testing_api.test_generators.ambiegen.Utils.road_gen import RoadGen


class GenerateTestCaseSampling(Sampling):

    """
    Module to generate the initial population
    """

    def _do(self, problem, n_samples, **kwargs):
        generator = RoadGen(
            cf.model["map_size"], cf.model["min_len"], cf.model["max_len"], cf.model["min_angle"], cf.model["max_angle"]
        )
        X = np.full((n_samples, 1), None, dtype=np.object)

        for i in range(n_samples):
            states = generator.test_case_generate()
            s = Solution()
            s.states = states
            X[i, 0] = s
        return X
