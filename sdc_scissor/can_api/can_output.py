import abc
import logging

import can
import click

from sdc_scissor.config import CONFIG


class ICANBusOutput(abc.ABC):
    @abc.abstractmethod
    def output_can_msg(self, msg):
        pass


class NoCANBusOutput(ICANBusOutput):
    def output_can_msg(self, msg):
        pass


class AbstractOutputDecorator(ICANBusOutput, abc.ABC):
    def __init__(self, wrappee: ICANBusOutput):
        self.wrappee = wrappee

    @abc.abstractmethod
    def output_can_msg(self, msg):
        pass


class CANBusOutputDecorator(AbstractOutputDecorator):
    def __init__(self, wrappee: ICANBusOutput):
        super().__init__(wrappee)
        # Configuration is according to: https://python-can.readthedocs.io/en/stable/bus.html
        self.bus = can.interface.Bus(
            interface=CONFIG.CAN_INTERFACE, channel=CONFIG.CAN_CHANNEL, bitrate=CONFIG.CAN_BITRATE
        )

    def output_can_msg(self, msg):
        try:
            self.bus.send(msg)
        except can.CanError as err:
            logging.error(err)
        self.wrappee.output_can_msg(msg)


class StdOutDecorator(AbstractOutputDecorator):
    """
    StdOutDecorator Objects are used to offer a flexible output_handler for th CAN messages.
    """

    def __init__(self, wrappee: ICANBusOutput):
        super().__init__(wrappee)

    def output_can_msg(self, msg):
        """
        Decorator class to output CAN messages to the console

        :param msg: The CAN message that should be sent to the output_handler.
        :return:
        """
        click.echo(click.style(msg, fg="green"))
