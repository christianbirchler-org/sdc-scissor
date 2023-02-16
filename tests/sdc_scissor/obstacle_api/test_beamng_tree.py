import logging

from beamngpy import StaticObject

from sdc_scissor.obstacle_api.beamng_tree import BeamngTree


class TestBeamngTree:
    def setup_class(self):
        pass

    def teardown_class(self):
        pass

    def setup_method(self):
        self.beamng_tree = BeamngTree()

    def test_get_new_beamng_tree(self, mocker):

        self.beamng_tree.x_pos = 100
        self.beamng_tree.y_pos = 100
        self.beamng_tree.z_pos = 0

        expected = StaticObject(
            name="test",
            pos=(100, 100, 0),
            rot=0,
            rot_quat=0,
            scale=(0.25, 0.25, 0.25),
            shape="/levels/west_coast_usa/art/shapes/trees/trees_conifer/BBZ_redwood1.dae",
        ).pos

        actual = self.beamng_tree.get().pos
        assert expected == actual


if __name__ == "__main__":
    logging.info("test_beamng_tree.py")
