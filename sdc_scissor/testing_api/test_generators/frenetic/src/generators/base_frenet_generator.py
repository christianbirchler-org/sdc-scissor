from sdc_scissor.testing_api.test_generators.frenetic.src.generators.base_generator import BaseGenerator
import sdc_scissor.testing_api.test_generators.frenetic.src.utils.frenet as frenet
import numpy as np
import logging as log


class BaseFrenetGenerator(BaseGenerator):
    def __init__(self, time_budget=None, executor=None, map_size=None, margin=10, strict_father=False):
        # Margin size w.r.t the map
        self.margin = margin
        self.recent_count = 0
        super().__init__(time_budget=time_budget, executor=executor, map_size=map_size, strict_father=strict_father)

    def kappas_to_road_points(self, kappas, frenet_step=10, theta0=1.57):
        """
        Args:
            kappas: list of kappa values
            frenet_step: The distance between to points.
            theta0: The initial angle of the line. (1.57 == 90 degrees)
        Returns:
            road points in cartesian coordinates
        """
        # Using the bottom center of the map.
        y0 = self.margin
        x0 = self.map_size / 2
        ss = np.arange(y0, (len(kappas) * frenet_step), frenet_step)

        # Transforming the frenet points to cartesian
        (xs, ys) = frenet.frenet_to_cartesian(x0, y0, theta0, ss, kappas)
        road_points = self.reframe_road(xs, ys)
        return road_points

    def execute_frenet_test(self, kappas, method="random", frenet_step=10, theta0=1.57, parent_info={}, extra_info={}):
        extra_info["kappas"] = kappas
        road_points = self.kappas_to_road_points(kappas, frenet_step=frenet_step, theta0=theta0)
        return road_points
        # if road_points:
        #     self.recent_count += 1
        #     return self.execute_test(road_points, method=method, parent_info=parent_info, extra_info=extra_info)
        # else:
        #     return 'CANNOT_REFRAME', None

    def reframe_road(self, xs, ys):
        """
        Args:
            xs: cartesian x coordinates
            ys: cartesian y coordinates
        Returns:
            A representation of the road that fits the map size (when possible).
        """
        min_xs = min(xs)
        min_ys = min(ys)
        road_width = self.margin  # TODO: How to get the exact road width?
        if (max(xs) - min_xs + road_width > self.map_size - self.margin) or (
            max(ys) - min_ys + road_width > self.map_size - self.margin
        ):
            log.info("Skip: Road won't fit")
            return None
            # TODO: Fail the entire test and start over
        xs = list(map(lambda x: x - min_xs + road_width, xs))
        ys = list(map(lambda y: y - min_ys + road_width, ys))
        return list(zip(xs, ys))
