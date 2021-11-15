import os

import matplotlib.pyplot as plt

from deeper.Deeper_test_generator.beamng_member import BeamNGMember
from deeper.Deeper_test_generator.road_bbox import RoadBoundingBox
from self_driving.road_polygon import RoadPolygon


def create_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def plot_road_bbox(road_bbox: RoadBoundingBox, fig=None, show=False, fill_color="white", border_color="black",
                   margin_percentage=0.01):
    if fig is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.margins(margin_percentage)
        plt.gca().set_aspect('equal', adjustable='box')
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        ax.axis('off')

    x, y = road_bbox.bbox.boundary.xy

    plt.fill(x, y, fill_color)
    plt.plot(x, y, border_color, linewidth=0.5)

    if show:
        plt.show()

    return fig


def plot_road_polygon(road_polygon: RoadPolygon, title="RoadPolygon", show=True, fig=None, fill_color="gray",
                      middle_color="#fad201", border_color="white", is_final_road=False, margin_percentage=0.01,
                      save=False, folder_path="../data/images", file_name="road.jpg", img_format="jpg"):
    if fig is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.margins(margin_percentage)
        plt.gca().set_aspect('equal', adjustable='box')
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        ax.axis('off')

    if is_final_road:
        x, y = road_polygon.polygon.exterior.xy
        plt.fill(x, y, c=fill_color)
        plt.plot(x, y, c=border_color, linewidth=0.5)
        xs, ys, _zs, _ws = zip(*road_polygon.road_points.middle)
        plt.plot(xs, ys, c=middle_color, linewidth=0.5)
    else:
        for polygon in road_polygon.polygons:
            x, y = polygon.exterior.xy
            plt.plot(x, y, c="#107dac")

    plt.title(title)

    if save:
        create_if_not_exists(folder_path)
        plt.savefig(os.path.join(folder_path, file_name), format=img_format, bbox_inches='tight')

    if show:
        plt.show()

    return fig


def plot_road(beam_ng_member: BeamNGMember, title="Road", show=True, save=False, folder_path="../data/images",
              file_name="road.jpg", img_format="jpg"):
    fig = plot_road_bbox(beam_ng_member.road_bbox, show=False, fill_color="#76BA1B", border_color="black")
    road_polygon = RoadPolygon.from_nodes(beam_ng_member.sample_nodes)
    fig = plot_road_polygon(road_polygon, fig=fig, title=title, show=show, is_final_road=True, save=save,
                            folder_path=folder_path, file_name=file_name, img_format=img_format)
    return fig


if __name__ == "__main__":
    from .road_generator2 import RoadGenerator

    # plot_road_bbox(RoadBoundingBox((-250, 0, 250, 500)), show=True)
    # plot_road_bbox(RoadBoundingBox((-250, 0, 250, 500)), show=True, fill_color="yellow", border_color="green")
    # plot_road_bbox(RoadBoundingBox((-250, 0, 250, 500)), show=True, fill_color="blue", border_color="red")

    road = RoadGenerator(num_control_nodes=5).generate()

    # plot_road_polygon(RoadPolygon.from_nodes(road.control_nodes))
    # plot_road_polygon(RoadPolygon.from_nodes(road.sample_nodes))
    # plot_road_polygon(RoadPolygon.from_nodes(road.control_nodes), is_final_road=True, border_color="black")
    # plot_road_polygon(RoadPolygon.from_nodes(road.sample_nodes), is_final_road=True, border_color="black")
    # plot_road_polygon(RoadPolygon.from_nodes(road.sample_nodes), is_final_road=True, border_color="red",
    #                   middle_color="blue", fill_color="green", title="Sample nodes (final)")
    # plot_road_polygon(RoadPolygon.from_nodes(road.sample_nodes), is_final_road=False, border_color="red",
    #                   middle_color="blue", fill_color="green", title="Sample nodes")
    #
    # plot_road(road)
    plot_road(road, save=True, show=False)
