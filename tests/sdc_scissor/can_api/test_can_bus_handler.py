import random
from pathlib import Path

from sdc_scissor.can_api.can_bus_handler import CanBusHandler
from sdc_scissor.can_api.can_output import NoCANBusOutput
from sdc_scissor.config import CONFIG


class TestCanBusHandler:
    def setup_class(self):
        pass

    def test_data_to_stdout_transmission(self, mocker):
        candb_file_path = Path(__file__).parent.parent.parent.parent / "sample_candb" / "beamng_pipeline_sample.dbc"
        can_dbc_map_path = Path(__file__).parent.parent.parent.parent / "dbc_maps" / "dbc_map_beamng.json"
        CONFIG.config = {
            "canbus": False,
            "can_dbc": candb_file_path,
            "can_dbc_map": can_dbc_map_path,
            "can_interface": "",
            "can_bitrate": "",
        }
        output_handler = NoCANBusOutput()
        can_bus_handler = CanBusHandler(output_handler=output_handler)

        data = {"wheelspeed": 50}
        can_bus_handler.transmit_sensor_data_to_can_bus(data=data)

    def test_encoded_and_decoded_CAN_wheelspeed_messages_should_be_equal(self, mocker):
        candb_file_path = Path(__file__).parent.parent.parent.parent / "sample_candb" / "beamng_pipeline_sample.dbc"
        can_dbc_map_path = Path(__file__).parent.parent.parent.parent / "dbc_maps" / "dbc_map_beamng.json"
        CONFIG.config = {
            "canbus": False,
            "can_dbc": candb_file_path,
            "can_dbc_map": can_dbc_map_path,
            "can_interface": "",
            "can_bitrate": "",
        }
        output_handler = NoCANBusOutput()
        can_bus_handler = CanBusHandler(output_handler=output_handler)
        db = can_bus_handler.db
        for _ in range(9000):
            wheelspeed = random.randint(0, 9000)
            data = {"wheelspeed": wheelspeed}
            for msg_specs in db.messages:
                if not msg_specs.frame_id == 177:
                    continue
                encoded_msg = db.encode_message(msg_specs.frame_id, data=data)
                decoded_msg = db.decode_message(msg_specs.frame_id, data=encoded_msg)
                print(decoded_msg)
                assert decoded_msg == data
