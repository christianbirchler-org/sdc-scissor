# this class must have simple fields in order to be serialized
from deeper.Deeper_test_generator.config import Config


# this class must have simple fields in order to be serialized
class BeamNGConfig(Config):
    EVALUATOR_LOCAL_BEAMNG = 'EVALUATOR_LOCAL_BEAMNG'

    def __init__(self):
        super().__init__()

        self.num_control_nodes = 10

        self.MAX_ANGLE = 40
        self.NUM_SPLINE_NODE = 20
        self.SEG_LENGTH = 25

        self.MIN_SPEED = 10
        self.MAX_SPEED = 70

        self.beamng_close_at_iteration = False
        self.beamng_evaluator = self.EVALUATOR_LOCAL_BEAMNG
