class _Config:
    def __init__(self):
        self.config = None

    @property
    def BEAMNG_HOME(self):
        return self.config["home"]

    @property
    def BEAMNG_USER(self):
        return self.config["user"]

    @property
    def RISK_FACTOR(self):
        return self.config["rf"]

    @property
    def MAX_SPEED(self):
        return self.config["max_speed"]

    @property
    def FIELD_OF_VIEW(self):
        return self.config["field_of_view"]

    @property
    def HAS_CAN_BUS(self):
        return self.config["canbus"]

    @property
    def CAN_DBC_PATH(self):
        return self.config["can_dbc"]

    @property
    def CAN_DBC_MAP_PATH(self):
        return self.config["can_dbc_map"]


CONFIG = _Config()
