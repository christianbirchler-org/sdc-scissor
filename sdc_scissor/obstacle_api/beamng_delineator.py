import logging

from beamngpy import ProceduralCylinder

from sdc_scissor.obstacle_api.delineator import Delineator


class BeamngDelineator(Delineator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self):
        return ProceduralCylinder(
            name="pyCylinder",
            pos=(self.x_pos, self.y_pos, self.z_pos),
            rot=self.rot,
            rot_quat=self.rot_quat,
            radius=self.radius,
            height=self.height,
        )


if __name__ == "__main__":
    logging.info("beamng_delineator.py")
