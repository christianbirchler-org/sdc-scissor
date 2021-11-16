class Config:
    GEN_RANDOM = 'GEN_RANDOM'
    GEN_RANDOM_SEEDED = 'GEN_RANDOM_SEEDED'
    GEN_SEQUENTIAL_SEEDED = 'GEN_SEQUENTIAL_SEEDED'

    SEG_LENGTH = 25
    NUM_SPLINE_NODES = 10
    INITIAL_NODE = (0.0, 0.0, -28.0, 8.0)
    ROAD_BBOX_SIZE = (-250, 0, 250, 500)

    def __init__(self):
        self.experiment_name = 'exp'
        self.fitness_weights = (1.0, -1.0)

        self.POPSIZE = 12
        self.NUM_GENERATIONS = 1000

        self.RESEED_UPPER_BOUND = int(self.POPSIZE * 0.1)

        self.MUTATION_EXTENT = 6.0
        self.ARCHIVE_THRESHOLD = 20.0

        self.K_SD = 0.01

        self.simulation_save = True
        self.simulation_name = 'beamng/sim_$(id)'

        self.keras_model_file = 'self-driving-car-185-2020.h5'

        # self.generator_name = Config.GEN_RANDOM
        self.generator_name = Config.GEN_RANDOM_SEEDED
        # self.generator_name = Config.GEN_SEQUENTIAL_SEEDED
        self.seed_folder = 'Seed_Population'
