import logging
import abc


class Delineator(abc.ABC):
    def __init__(self, x_pos=None, y_pos=None, z_pos=None, radius=0.2, height=1.0, rot=None, rot_quat=(0, 0, 0, 1)):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        self.radius = radius
        self.height = height
        self.rot = rot
        self.rot_quat = rot_quat

    @abc.abstractmethod
    def get(self):
        pass


if __name__ == "__main__":
    logging.info("delineator.py")
