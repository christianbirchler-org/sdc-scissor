import math
from sdc_scissor.testing_api.test_generators.frenetic_v.src.generators.base_generator import BaseGenerator
from sdc_scissor.testing_api.test_generators.frenetic_v.src.utils import frenet

from shapely import geometry, affinity


import numpy as np
import logging as log


class BaseFrenetVGenerator(BaseGenerator):
    def __init__(
        self,
        executor=None,
        map_size=None,
        segment_length=10,
        lane_width=4,
        strict_father=False,
        store_additional_data=False,
    ):
        # Margin size w.r.t the map
        self.segment_length = segment_length
        self.lane_width = lane_width
        self.margin = 10  # to be safe... there were some out of margin with (lane_width * 2)
        self.recent_count = 0
        self.theta0 = 1.57  # theta0: The initial angle of the line. (1.57 == 90 degrees)
        super().__init__(
            executor=executor,
            map_size=map_size,
            strict_father=strict_father,
            store_additional_data=store_additional_data,
        )

    def kappas_to_road_points(self, kappas) -> np.array:
        """
        The FreneticV main algorithm.

        :param kappas: list of kappa values
        :return: road points in cartesian coordinates
        """
        # Using the bottom center of the map.
        y0 = self.margin
        x0 = self.map_size / 2
        theta0 = self.theta0
        ss = np.cumsum([self.segment_length] * len(kappas)) - self.segment_length
        # Transforming the frenet points to cartesian
        (xs, ys) = frenet.frenetv_to_cartesian(x0, y0, theta0, ss, kappas)

        return np.column_stack([xs, ys])

    def execute_frenet_test(self, kappas, method="random", parent_info={}, extra_info={}):
        extra_info["kappas"] = kappas
        road_points = self.kappas_to_road_points(kappas)

        # Pre-validation
        # 1. check self-intersection
        if self.is_likely_self_intersecting(road_points):
            return "LIKELY_SELF_INTERSECTING", None

        # 2. check if it a) fits into map-dimensions and b) if we can transform it to be inside the map
        road_points = self.reframe_road(road_points)

        if road_points is not None:
            self.recent_count += 1
            # Transforming numpy array to list of tuples
            road_points_list = list(map(tuple, road_points))
            # return self.execute_test(road_points_list, method=method, parent_info=parent_info, extra_info=extra_info)
            return road_points_list
        else:
            return "CANNOT_REFRAME", None

    def is_likely_self_intersecting(self, road_points) -> bool:
        center_line = geometry.LineString(road_points)

        left_line = center_line.parallel_offset(self.lane_width, "left")
        right_line = center_line.parallel_offset(self.lane_width, "right")

        drop_road_checks = {
            "left_complex": not left_line.is_simple,
            "center_complex": not center_line.is_simple,
            "right_complex": not right_line.is_simple,
            "left_int_right": left_line.intersects(right_line),
            "right_int_left": right_line.intersects(left_line),
            "left_ring": left_line.is_ring,
            "center_ring": center_line.is_ring,
            "right_ring": right_line.is_ring,
            "left_is_multi": left_line.geom_type != "LineString",
            "right_is_multi": right_line.geom_type != "LineString",
        }

        return any(drop_road_checks.values())

    def rotate_and_relocate_line(self, center_line, orientation):
        reoriented_center = affinity.rotate(center_line, orientation)
        reoriented_convex_hull = reoriented_center.convex_hull
        reoriented_convex_hull_coords = np.array(reoriented_convex_hull.exterior.coords)

        xoff = self.margin - min(reoriented_convex_hull_coords[:, 0])  # where's the left side?
        yoff = self.margin - min(reoriented_convex_hull_coords[:, 1])  # where's the bottom?
        new_center_line = affinity.translate(reoriented_center, xoff=xoff, yoff=yoff)
        return new_center_line

    def reframe_road(self, road_points):
        center_line = geometry.LineString(road_points)

        reduced_map_rect = geometry.Polygon(
            [
                (self.margin, self.margin),
                (self.margin, self.map_size - self.margin),
                (self.map_size - self.margin, self.map_size - self.margin),
                (self.map_size - self.margin, self.margin),
            ]
        )

        # check if the line is in the map already
        if reduced_map_rect.contains(center_line):
            log.debug("The road already fits.")
            return road_points

        # rotation and alignment

        # Aligning based on best-fit orientation of two rectangles
        # https://math.stackexchange.com/questions/3179927/determining-best-angle-of-rotation-to-fit-a-rectangle-inside-a-rectangle
        # l = geometry.LineString(rectangular_hull_coords[0:2]).length
        # b = geometry.LineString(rectangular_hull_coords[1:3]).length
        # orientation = math.acos(self.map_size / math.sqrt(l ** 2 + b ** 2)) + math.atan(b / l)
        # new_center_line = self.rotate_and_relocate_line(center_line, orientation)

        # If aligning rectangles does not always work...
        for orientation in range(0, 90, 1):
            new_center_line = self.rotate_and_relocate_line(center_line, orientation)
            if reduced_map_rect.contains(new_center_line):
                log.info("Road was relocated and rotated")
                return np.array(new_center_line.coords)

        log.info("The road could not be fit within the boundaries.")
        return None
