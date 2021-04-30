import numpy as np


def get_node_coords(node):
    return node[0], node[1], node[2]


def points_distance(p1, p2):
    return np.linalg.norm(np.subtract(get_node_coords(p1), get_node_coords(p2)))

