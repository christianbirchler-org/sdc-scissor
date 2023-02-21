import abc
import json
import logging
from pathlib import Path

import can
import cantools
import click

from sdc_scissor.config import CONFIG


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


class ICANBusOutput(abc.ABC):
    @abc.abstractmethod
    def output_can_msg(self, msg):
        pass


class NoCANBusOutput(ICANBusOutput):
    def output_can_msg(self, msg):
        pass


class CANBusOutput(ICANBusOutput):
    def __init__(self):
        # Configuration is according to: https://python-can.readthedocs.io/en/stable/bus.html
        self.bus = can.interface.Bus(
            interface=CONFIG.CAN_INTERFACE, channel=CONFIG.CAN_CHANNEL, bitrate=CONFIG.CAN_BITRATE
        )

    def output_can_msg(self, msg):
        try:
            self.bus.send(msg)
        except can.CanError as err:
            logging.error(err)


class StdOut(ICANBusOutput):
    """
    StdOut Objects are used to offer a flexible output_handler for th CAN messages.
    """

    def __init__(self):
        print("Init Can Bus Output")

        self.output_logger = logging.getLogger("CAN_OUT_LOG")
        fh = logging.FileHandler("can_out.log")
        fh.setLevel(logging.DEBUG)
        self.output_logger.addHandler(fh)

    def output_can_msg(self, msg):
        """
        This method is used to output_handler the can message. It is called by the CanBusHandler.
        The current output_handler source is a python logger.

        :param msg: The CAN message that should be sent to the output_handler.
        :return:
        """
        # self.output_logger.info(msg)
        click.echo(click.style(msg, fg="green"))


class CanBusHandler:
    """
    CanBusHandler Objects can be used to receive data from a simulation and generate CAN messages from it.
    """

    def __init__(self, output_handler: ICANBusOutput):
        logging.info("Init CanBusHandler")
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
        It will then generate CAN messages from the data and send them to the StdOut.

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

            # Generate the CAN message
            frame_data = example_msg.encode(frame_values)
            msg = can.Message(arbitration_id=frame_id, data=frame_data)

            # Send the message to the StdOut
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
