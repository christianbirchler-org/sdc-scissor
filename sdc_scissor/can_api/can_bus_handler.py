import json
import logging
import time
from pathlib import Path

import can
import cantools

from sdc_scissor.can_api.can_output import ICANBusOutput
from sdc_scissor.config import CONFIG

_logger = logging.getLogger(__file__)


def get_can_frame_list(can_db):
    """
    Returns a list of all sample frames in the given can database

    :param can_db: The CAN database
    :return: A list of all sample frames in the given can database
    """
    can_frame_list = []
    for can_msg in can_db.messages:
        # For each message in the database store it's information in a dictionary and add it to the list
        signal_list = []

        # Get the id of the frame
        frame_id = can_msg.frame_id

        # Get all signals for this frame and store them in the signal_list
        for signal in can_msg.signals:
            signal_list.append(signal.name)

        # Store the information in the dictionary and add it to the frame_list
        res = {"example_message": can_msg, "frame_id": frame_id, "signal_list": signal_list}
        can_frame_list.append(res)

    return can_frame_list


class CanBusHandler:
    """
    CanBusHandler Objects can be used to receive data from a simulation and generate CAN messages from it.
    """

    def __init__(self, output_handler: ICANBusOutput):
        logging.debug("Init CanBusHandler")
        # Load the config file

        # Load the CAN database
        db_path = CONFIG.CAN_DBC_PATH
        dbc_map_path = CONFIG.CAN_DBC_MAP_PATH
        db = cantools.db.load_file(Path(db_path))

        # Gather the sample frames from the dbc
        self.frame_list = get_can_frame_list(db)
        self.output_handler = output_handler

        # Load the dbc map used to map the simulation signals to the dbc signals
        with open(dbc_map_path) as f:
            self.dbc_map = json.load(f)

    def transmit_sensor_data_to_can_bus(self, data):
        """
        This method should be called by a TestRunner with the current data from the simulation.
        It will then generate CAN messages from the data and send them to the StdOutDecorator.

        :param data: A dictionary containing the current data from the simulation.
        :return:
        """ ""

        for frame in self.frame_list:
            # For each frame in the CAN db we transform the values using the dbc_map and then generate the message

            example_msg = frame["example_message"]
            frame_id = frame["frame_id"]
            frame_sig_list = frame["signal_list"]

            # Transform the simulation values to assure they are within the dbc range and named correctly
            frame_values = self.get_frame_values(frame_sig_list, data)
            _logger.debug("can frame data values: {}".format(frame_values))

            # Generate the CAN message
            frame_data = example_msg.encode(frame_values)
            _logger.debug("can frame data encoded: {}".format(frame_data))
            msg = can.Message(arbitration_id=frame_id, data=frame_data)
            msg.timestamp = time.time()

            self.send_can_msg(msg)

    def send_can_msg(self, msg):
        self.output_handler.output_can_msg(msg)

    def get_frame_values(self, frame_signal_list, data):
        """
        This method transforms the simulation values to assure they are within the dbc range and named correctly.

        :param frame_signal_list: A list of the signals in the frame
        :param data: A dictionary containing the current data from the simulation.
        :return: A dictionary containing the values for the frame named correctly and within the dbc range.
        """
        values = {}
        for signal in frame_signal_list:
            # For each signal in the frame we transform the value using the dbc_map

            # Gather the dbc signal range and default value
            default = self.dbc_map[signal]["default"]
            s_min = self.dbc_map[signal]["min"]
            s_max = self.dbc_map[signal]["max"]

            if self.dbc_map[signal]["sim_signal_name"] in data:
                # Check if the value exists in the simulation data
                v = data[self.dbc_map[signal]["sim_signal_name"]]
                if s_min <= v <= s_max:
                    # Check if the value is within the defined range
                    values[signal] = v
                else:
                    # If the value is not within the defined range we use the default value
                    values[signal] = default
            else:
                # If the value does not exist in the simulation data we use the default value
                values[signal] = default

        return values
