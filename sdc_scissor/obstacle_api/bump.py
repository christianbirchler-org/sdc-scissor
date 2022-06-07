import logging
import abc


class Bump(abc.ABC):
    def __init__(
        self,
        x_pos=None,
        y_pos=None,
        z_pos=None,
        width=6,
        length=2,
        height=0.2,
        upper_length=1,
        upper_width=2,
        rot=None,
        rot_quat=(0, 0, 0, 1),
    ):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        self.width = width
        self.length = length
        self.height = height
        self.upper_length = upper_length
        self.upper_width = upper_width
        self.rot = rot
        self.rot_quat = rot_quat

    @abc.abstractmethod
    def get(self):
        pass


if __name__ == "__main__":
    logging.info("bump.py")
