import logging

from sdc_scissor.obstacle_api.beamng_tree import BeamngTree
from beamngpy import StaticObject


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

        expected = mocker.patch("StaticObject")
        actual = self.beamng_tree.get()
        assert expected == actual


if __name__ == "__main__":
    logging.info("test_beamng_tree.py")
