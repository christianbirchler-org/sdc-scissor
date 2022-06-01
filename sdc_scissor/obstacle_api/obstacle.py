import logging

from beamngpy import ProceduralBump, ProceduralCylinder


class Obstacle:
    pass


class Bump(Obstacle):
    def __init__(self, x_pos=None, y_pos=None, width=6, length=2, height=0.2, upper_length=1, upper_width=2, rot=None,
                 rot_quat=(0, 0, 0, 1)):
        """

        :param x_pos: x position
        :param y_pos: y position
        :param width: width of Obstacle
        :param length:  length of Obstacle
        :param height:  length of Obstacle
        :param upper_length:  upper length of Obstacle
        :param upper_width:  upper width of Obstacle
        :param rot:
        :param rot_quat:
        """

        self.width = width
        self.length = length
        self.height = height
        self.upper_length = upper_length
        self.upper_width = upper_width
        self.rot = rot
        self.rot_quat = rot_quat
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_beamng_obstacle_object(self):
        """
        Create Bump Obstacle
        """
        logging.info('get_beamng_obstacle_object')
        pos = self.x_pos, self.y_pos, -28
        return ProceduralBump(name='pybump', pos=pos, rot=self.rot, rot_quat=self.rot_quat,
                              width=self.width, length=self.length, height=self.height, upper_length=self.upper_length,
                              upper_width=self.upper_width)


class Delineator(Obstacle):
    def __init__(self, x_pos=None, y_pos=None, radius=0.2, height=1.0, rot=None, rot_quat=(0, 0, 0, 1)):
        """

        :param x_pos: x position
        :param y_pos: y position
        :param radius: radius of Obstacle
        :param height:  height of Obstacle
        :param rot:
        :param rot_quat:
        """
        self.radius = radius
        self.height = height
        self.rot = rot
        self.rot_quat = rot_quat
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_beamng_obstacle_object(self):
        """
        Create Cylinder Obstacle
        """
        pos = self.x_pos, self.y_pos, -28
        return ProceduralCylinder(name='pyCylinder', pos=pos, rot=self.rot,
                                  rot_quat=self.rot_quat, radius=self.radius, height=self.height)


if __name__ == '__main__':
    logging.info('obstacle.py')
