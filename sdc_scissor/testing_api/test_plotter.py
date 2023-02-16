import abc

import matplotlib.pyplot as plt

from sdc_scissor.testing_api.road_model import RoadModel


class TestPlotter(abc.ABC):
    def plot(self, *args):
        pass


class NullTestPlotter(TestPlotter):
    pass


class TestPlotter(TestPlotter):
    def __init__(self):
        pass

    def plot(self, road_model: RoadModel):
        x_center_line = [i[0] for i in road_model.coordinates]
        y_center_line = [i[1] for i in road_model.coordinates]
        right_line = road_model.center_line.parallel_offset(side="right", distance=5.0)
        left_line = road_model.center_line.parallel_offset(side="left", distance=5.0)

        x_right_line = []
        y_right_line = []
        for i in range(0, round(right_line.length)):
            interpolated_point_right_line = right_line.interpolate(i)
            x_right_line.append(interpolated_point_right_line.x)
            y_right_line.append(interpolated_point_right_line.y)

        x_left_line = []
        y_left_line = []
        for i in range(0, round(left_line.length)):
            interpolated_point_left_line = left_line.interpolate(i)
            x_left_line.append(interpolated_point_left_line.x)
            y_left_line.append(interpolated_point_left_line.y)

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.plot(x_center_line, y_center_line, color="#ebba34", linewidth=2.0, label="center line")
        ax.plot(x_left_line, y_left_line, color="black", linewidth=2.0, label="left line")
        ax.plot(x_right_line, y_right_line, color="black", linewidth=2.0, label="right line")
        ax.plot([x_center_line[0]], [y_center_line[0]], "o", color="green", label="start")
        ax.plot([x_center_line[-1]], [y_center_line[-1]], "*", color="red", label="end")
        ax.legend()
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        plt.show()
