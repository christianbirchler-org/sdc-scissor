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
    def CAN_STDOUT(self):
        return self.config["can_stdout"]

    @property
    def CAN_DBC_PATH(self):
        return self.config["can_dbc"]

    @property
    def CAN_DBC_MAP_PATH(self):
        return self.config["can_dbc_map"]

    @property
    def CAN_INTERFACE(self):
        return self.config["can_interface"]

    @property
    def CAN_CHANNEL(self):
        return self.config["can_channel"]

    @property
    def CAN_BITRATE(self):
        return self.config["can_bitrate"]

    @property
    def INFLUXDB_BUCKET(self):
        return self.config["influxdb_bucket"]

    @property
    def INFLUXDB_ORG(self):
        return self.config["influxdb_org"]

    @property
    def EXECUTION_START_TIME(self):
        return self.config["execution_start_date_time"]

    @property
    def CURRENT_TEST_ID(self):
        return self.config["current_test_id"]


CONFIG = _Config()
