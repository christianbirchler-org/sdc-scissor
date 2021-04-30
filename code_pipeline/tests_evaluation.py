import logging

from shapely.geometry import Point, LineString
from shapely.ops import nearest_points

from self_driving.edit_distance_polyline import iterative_levenshtein

from self_driving.simulation_data import SimulationDataRecord

from scipy.interpolate import splev, splprep

import numpy as np

from itertools import combinations

from numpy.ma import arange

from math import sqrt

from itertools import islice
import functools
import os
import json

BEFORE_THRESHOLD = 60.0
AFTER_THRESHOLD = 20.0

# The following utility methods might not even be used. TODO Clean up if possible

def _interpolate_and_resample_splines(sample_nodes, nodes_per_meter = 1, smoothness=0, k=3, rounding_precision=4):
    """ Interpolate a list of points as a spline (quadratic by default) and resample it with num_nodes"""

    # Compute lenght of the road
    road_lenght = LineString([(t[0], t[1]) for t in sample_nodes]).length

    num_nodes = nodes_per_meter  * int(road_lenght)

    old_x_vals = [t[0] for t in sample_nodes]
    old_y_vals = [t[1] for t in sample_nodes]
    # old_width_vals  = [t[3] for t in sample_nodes]

    # Interpolate the old points
    pos_tck, pos_u = splprep([old_x_vals, old_y_vals], s=smoothness, k=k)

    # Resample them
    step_size = 1 / num_nodes
    unew = arange(0, 1 + step_size, step_size)

    new_x_vals, new_y_vals = splev(unew, pos_tck)

    # Reduce floating point rounding errors otherwise these may cause problems with calculating parallel_offset
    return list(zip([round(v, rounding_precision) for v in new_x_vals],
                    [round(v, rounding_precision) for v in new_y_vals],
                    # TODO Brutally hard-coded
                    [-28.0 for v in new_x_vals],
                    [8.0 for w in new_x_vals]))


def _find_circle_and_return_the_center_and_the_radius(x1, y1, x2, y2, x3, y3):
    """THIS IS ONLY TO AVOID BREAKING OLD CODE"""
    x12 = x1 - x2;
    x13 = x1 - x3;

    y12 = y1 - y2;
    y13 = y1 - y3;

    y31 = y3 - y1;
    y21 = y2 - y1;

    x31 = x3 - x1;
    x21 = x2 - x1;

    # x1^2 - x3^2
    sx13 = pow(x1, 2) - pow(x3, 2);

    # y1^2 - y3^2
    sy13 = pow(y1, 2) - pow(y3, 2);

    sx21 = pow(x2, 2) - pow(x1, 2);
    sy21 = pow(y2, 2) - pow(y1, 2);

    f = (((sx13) * (x12) + (sy13) *
          (x12) + (sx21) * (x13) +
          (sy21) * (x13)) // (2 *
                              ((y31) * (x12) - (y21) * (x13))));

    g = (((sx13) * (y12) + (sy13) * (y12) +
          (sx21) * (y13) + (sy21) * (y13)) //
         (2 * ((x31) * (y12) - (x21) * (y13))));

    c = (-pow(x1, 2) - pow(y1, 2) -
         2 * g * x1 - 2 * f * y1);

    # eqn of circle be x^2 + y^2 + 2*g*x + 2*f*y + c = 0
    # where centre is (h = -g, k = -f) and
    # radius r as r^2 = h^2 + k^2 - c
    h = -g;
    k = -f;
    sqr_of_r = h * h + k * k - c;

    # r is the radius
    r = round(sqrt(sqr_of_r), 5);

    return ((h, k), r)


    #print("Centre = (", h, ", ", k, ")");
    #print("Radius = ", r);
    #print("Radius = ", degrees(r));


def _road_segments_grouper(iterable, radius_tolerance=0.3):
    """
        Group road segments by similarity. Similarity is defined by type, radius and the distance between
        interpolating circle centers
    """
    prev = None
    group = []
    next_index = -1
    for index, item in enumerate(iterable):

        if index < next_index:
            continue
        if index == next_index:
            # Initialize the group with the element we identified two steps ago
            group.append(item)
            prev = item
            continue

        # Create a new group if this is the first element
        if not prev:
            group.append(item)
        elif prev["type"] == "straight" and item["type"] == "straight":
            group.append(item)
        elif prev["type"] == "straight" and item["type"] == "turn" or \
                prev["type"] == "turn" and item["type"] == "straight":
            # print("Returning group", prev["type"], "->", item["type"], group)
            # Return the current group
            yield group
            # Prepare the next group
            # prev = None
            group = []
            # Skip then next two elements
            next_index = index + 2
            continue
        else:

            assert prev["type"] != "straight"
            assert item["type"] != "straight"

            perc_diff_prev = abs(prev["radius"] - item["radius"]) / prev["radius"]
            perc_diff_item = abs(prev["radius"] - item["radius"]) / item["radius"]
            distance_between_centers = Point(prev["center"][0], prev["center"][1]).distance( Point(item["center"][0], item["center"][1]))
            if perc_diff_prev < radius_tolerance and perc_diff_item < radius_tolerance and \
                distance_between_centers < prev["radius"] and distance_between_centers < item["radius"]:
                group.append(item)
            else:
                # print("Returning group", prev["type"], "->", item["type"], group)
                # Return the current group
                yield group
                # Prepare the next group
                # prev = None
                group = []
                # Skip then next two elements
                next_index = index + 2
                continue

        prev = item

    # Not sure about this one...
    # Might cause consecutive straights to be reported?
    if group:
        # print("Returning last group ", group)
        # print("\n\n\n")
        yield group


# Merge two segments, but keeping the attributes from the first, but the points from everybody without duplicates
# This cannot be easily fit into a lambda
def _merge_segments_points(s1, s2):
    s1["points"].append(s2["points"][-1])
    return s1


def _merge_segments(s1, s2):
    s1["points"].extend(s2["points"])
    return s1


def _window(seq, n=2):
    """
    Returns a sliding window (of width n) over data from the iterable
       s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
    Taken from: https://stackoverflow.com/questions/6822725/rolling-or-sliding-window-iterator

    :param seq:
    :param n:
    :return:
    """

    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def _identify_segments(nodes):
    """
        Return grouping of nodes. Each group correspond to a segment [[][]]
        Assumptions: Lines are smooth, so there's no two consecutive straight segments that are not divided
        by a turn.

    """
    assert len(nodes) > 3, "not enough nodes"

    segments = []

    # Accumulate all the segments based on 3 points, and then simplify
    # Probably can do also p1, p2, p3 in ...
    for three_points in _window(nodes, n=3):

        center, radius = _find_circle_and_return_the_center_and_the_radius(
                                        three_points[0][0], three_points[0][1],#
                                        three_points[1][0], three_points[1][1], #
                                        three_points[2][0], three_points[2][1])

        if radius > 400:
            type = "straight"
            center = None
            radius = None
        else:
            type = "turn"

        current_segment = {}

        current_segment["type"] = type
        current_segment["center"] = center
        current_segment["radius"] = radius
        current_segment["points"] = []
        current_segment["points"].append(three_points[0])
        current_segment["points"].append(three_points[1])
        current_segment["points"].append(three_points[2])

        segments.append(current_segment)

    # Simplify the list of segments by grouping together similar elements
    # This procedure is flawed: it can report s->s but also spurios t->t (which are t->s). The issue is that
    # By looking at three points in isolation we can have confiugartions like this:
    # A, B, C -> s1
    # B, C, D -> t1
    # C, D, E -> t1 or s2 does not matter
    # D, E, F -> s2
    # E, F, G -> s2
    # The procedure understands that s1 is not compatible with t1 because of D, so it creates a group
    # Then skips two tripletted, so D becomes the first point (no overlap). But now the triplette is a straight not a turn...

    segments = list(_road_segments_grouper(segments))

    # Make sure you consider list of points and not triplettes.
    for index, segment in enumerate(segments[:]):
        # Replace the element with the merged one
        segments[index] = functools.reduce(lambda a, b: _merge_segments_points(a, b), segment)

    # Resolve and simplify. If two consecutive segments are straights we put them together.
    refined_segments = []

    # If two consecutive segments are similar we put them together
    for s in segments:
        if len(refined_segments) == 0:
            refined_segments.append(s)
        elif refined_segments[-1]["type"] == "straight" and s["type"] == "straight":
            # print("Merging ", refined_segments[-1], "and", s)
            # Take the points from the second segment put them into the first and return the first
            refined_segments[-1] = _merge_segments(refined_segments[-1], s)
        else:
            refined_segments.append(s)


    # At this point we have computed an approximation but we might need to smooth the edges, as
    # there might be little segments that could be attached to the previous ones

    # Associate small segments to prev/latest based on similarity
    segments = []

    # Move forward
    for index, segment in enumerate(refined_segments[:]):
        if len(segments) == 0:
            segments.append(segment)
        elif len(segment["points"]) <= 5:

            # Merge this segment to the previous one if they have the same type
            if segments[-1]["type"] == segment["type"]:
                segments[-1] = _merge_segments(segments[-1], segment)
            # Merge short straights into turns, but never turns into straights?
            else:
                segments.append(segment)
        else:
            segments.append(segment)

    # Repeat the process but moving backward
    refined_segments = segments[:]
    reversed(refined_segments)
    segments = []
    for index, segment in enumerate(refined_segments[:]):
        if len(segments) == 0:
            segments.append(segment)
        elif len(segment["points"]) <= 5:

            # Merge this segment to the previous one if they have the same type
            if segments[-1]["type"] == segment["type"]:
                segments[-1] = _merge_segments(segments[-1], segment)
            # Merge short straights into turns, but never turns into straights?
            else:
                segments.append(segment)
        else:
            segments.append(segment)

    reversed(segments)

    return segments


def _test_failed_with_oob(json_file):
    """
        Load the test from the json file and check the relevant attributes. The test must be valid, and FAILED because
        of OOB
    """
    with open(json_file, 'r') as test_json:
        data = json.load(test_json)
    return data["is_valid"] and data["test_outcome"] == "FAILED" and data["description"].startswith("Car drove out of the lane")



class RoadTestEvaluator:
    """
    This class identify the interesting segment for an OOB. The interesting segment is defined by that
    part of the road before and after an OOB defined by the values road_length_before_oob and
    roal_length_after_oob
    """

    def __init__(self, road_length_before_oob=BEFORE_THRESHOLD, road_lengrth_after_oob=AFTER_THRESHOLD):
        self.road_length_before_oob = road_length_before_oob
        self.road_lengrth_after_oob = road_lengrth_after_oob

    # Note execution data also contains the road
    def identify_interesting_road_segments(self, road_nodes, execution_data):
        # Interpolate and resample
        # TODO we also have already interpolated points
        road_points = _interpolate_and_resample_splines(road_nodes)

        # Create a LineString out of the road_points
        road_line = LineString([(rp[0], rp[1]) for rp in road_points])

        oob_pos = None
        # TODO This should be the last observation, so we should iterate the list from the last
        # Assuming we stop the execution at OBE
        positions = []
        for record in execution_data:
            positions.append(Point(record.pos[0], record.pos[1]))
            if record.is_oob:
                oob_pos = Point(record.pos[0], record.pos[1])
                break

        if oob_pos == None:
            # No oob, no interesting segments and we cannot tell whether the OOB was left/rigth
            return None, None, None, None

        # Find the point in the interpolated points that is closes to the OOB position
        # https://stackoverflow.com/questions/24415806/coordinates-of-the-closest-points-of-two-geometries-in-shapely
        np = nearest_points(road_line, oob_pos)[0]
        # Assuming that the road is made by one lane per traffic direction and position are collected frequently,
        # if the distance between oob and the center of the road is greater than 2.0 (half of lane) then the oob is
        # on the right side, otherwise on the left side
        #
        if oob_pos.distance(road_line) < 2.0:
            oob_side = "LEFT"
        else:
            oob_side = "RIGHT"

        # https://gis.stackexchange.com/questions/84512/get-the-vertices-on-a-linestring-either-side-of-a-point
        before = None
        after = None

        road_coords = list(road_line.coords)
        for i, p in enumerate(road_coords):
            if Point(p).distance(np) < 0.5:  # Since we interpolate at every meter, whatever is closer than half of if
                before = road_coords[0:i]
                before.append(np.coords[0])

                after = road_coords[i:]

        # Take the M meters 'before' the OBE or the entire segment otherwise
        distance = 0
        temp = []
        for p1, p2 in _window(reversed(before), 2):

            if len(temp) == 0:
                temp.append(p1)

            distance += LineString([p1, p2]).length

            if distance >= self.road_length_before_oob:
                break
            else:
                temp.insert(0, p2)

        segment_before = LineString(temp)

        distance = 0
        temp = []
        for p1, p2 in _window(after, 2):

            if len(temp) == 0:
                temp.append(p1)

            distance += LineString([p1, p2]).length

            if distance >= self.road_lengrth_after_oob:
                break
            else:
                temp.append(p2)

        segment_after = LineString(temp)

        # Identify the road segments from ALL the "interesting part of the road"
        # TODO Why do we need "segments" can't we simply return the (interpolated) road points?
        # interesting_road_segments = _identify_segments(list(segment_before.coords) + list(segment_after.coords))
        return oob_pos, segment_before, segment_after, oob_side


class OOBAnalyzer:
    """
        This class implements some analyses on the OOB discovered by a test generator. For the moment,
        we compute similarity of the OOBS using Levenstein distance over the "Interesting" segments
    """
    def __init__(self, result_folder):
        self.logger = logging.getLogger('OOBAnalyzer')
        self.oobs = self._load_oobs_from(result_folder)

    def _load_oobs_from(self, result_folder):

        # Go over all the files in the result folder and extract the interesing road segments for each OOB
        road_test_evaluation = RoadTestEvaluator(road_length_before_oob=30, road_lengrth_after_oob=30)

        oobs = []
        for subdir, dirs, files in os.walk(result_folder, followlinks=False):
            # Consider only the files that match the pattern
            for sample_file in sorted(
                    [os.path.join(subdir, f) for f in files if f.startswith("test.") and f.endswith(".json")]):

                self.logger.debug("Processing test file %s", sample_file)

                test_id, is_valid, test_outcome, road_data, execution_data = self._load_test_data(sample_file)


                # If the test is not valid or passed we skip it the analysis
                if not is_valid or not test_outcome == "FAIL":
                    self.logger.debug("\t Test is invalid")

                    continue

                # Extract data about OOB, if any
                oob_pos, segment_before, segment_after, oob_side = road_test_evaluation.identify_interesting_road_segments(
                    road_data, execution_data)

                # A test might fail also without OOB
                if oob_pos is None:
                    continue

                oobs.append(
                    {
                        'test id': test_id,
                        'simulation file': sample_file,
                        # Point
                        'oob point': oob_pos,
                        # LEFT/RIGHT
                        'oob side': oob_side,
                        # LineStrings representing the center of the road, interpolated points
                        'road segment before oob': segment_before,
                        'road segment after oob': segment_after,
                        # This is the list of points, so we need to extract from LineString objects
                        'interesting segment': list(segment_before.coords) + list(segment_after.coords)
                    }
                )

        self.logger.info("Collected data about %d oobs", len(oobs))
        return oobs

    def _load_test_data(self, execution_data_file):
        # Load the execution data
        with open(execution_data_file) as input_file:
            json_data = json.load(input_file)
            test_id = json_data["id"]
            road_data = json_data["road_points"]
            is_valid = json_data["is_valid"]
            if is_valid:
                test_outcome = json_data["test_outcome"]
                execution_data = [SimulationDataRecord(*record) for record in json_data["execution_data"]]
            else:
                test_outcome = None
                execution_data = []

        return test_id, is_valid, test_outcome, road_data, execution_data

    def _compute_sparseness(self):
        # Compute distance among the OOB and take the avg of their maximum distance
        max_distances_starting_from = {}

        for (oob1, oob2) in combinations(self.oobs, 2):
            # Compute distance between cells
            distance = iterative_levenshtein(oob1['interesting segment'], oob2['interesting segment'])
            self.logger.debug("Distance of OOB %s from OOB %s is %.3f", oob1["test id"], oob2["test id"], distance)

            # Update the max values
            if oob1['test id'] in max_distances_starting_from.keys():
                max_distances_starting_from[oob1['test id']] = max(
                    max_distances_starting_from[oob1['test id']], distance)
            else:
                max_distances_starting_from[oob1['test id']] = distance

        mean_distance = np.mean([list(max_distances_starting_from.values())]) if len(
            max_distances_starting_from) > 0 else np.NaN
        std_dev = np.std([list(max_distances_starting_from.values())]) if len(
            max_distances_starting_from) > 0 else np.NaN

        self.logger.debug("Sparseness: Mean: %.3f, StdDev: %3f", mean_distance, std_dev)

        return mean_distance, std_dev

    def _compute_oob_side_stats(self):
        n_left = 0
        n_right = 0

        for oob in self.oobs:
            if oob['oob side'] == "LEFT":
                n_left += 1
            else:
                n_right += 1

        self.logger.debug("Left: %d - Right: %d", n_left, n_right)
        return n_left, n_right

    def _analyse(self):
        """
            Iterate over the result_folder, identify the OOB and measure their relative distance, and ... TODO
        """
        mean_sparseness, stdev_sparseness = self._compute_sparseness()
        n_oobs_on_the_left, n_oobs_on_the_right = self._compute_oob_side_stats()

        report_data = {}

        report_data["sparseness"] = (mean_sparseness, stdev_sparseness)
        report_data["oob_side"] = (n_oobs_on_the_left, n_oobs_on_the_right)

        return report_data

    def create_summary(self):

        report_data = self._analyse()
        csv_header = "total_oob,left_oob,right_oob,avg_sparseness,stdev_sparseness"
        csv_body = "%d,%d,%d,%.3f,%3.f" % (len(self.oobs), *report_data["oob_side"],*report_data["sparseness"])

        return "\n".join([csv_header, csv_body])
