import logging

from beamngpy import ProceduralBump

from sdc_scissor.obstacle_api.bump import Bump


class BeamngBump(Bump):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self):
        return ProceduralBump(
            name="pybump",
            pos=(self.x_pos, self.y_pos, self.z_pos),
            rot=self.rot,
            rot_quat=self.rot_quat,
            width=self.width,
            length=self.length,
            height=self.height,
            upper_length=self.upper_length,
            upper_width=self.upper_width,
        )


if __name__ == "__main__":
    logging.info("beamng_bump.py")
