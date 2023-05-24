import abc
import math
import random

import can
import cantools.database

from sdc_scissor.config import CONFIG


class CANMessage:
    def __init__(self, **kwargs):
        self.__msg = can.Message(**kwargs)

    def __repr__(self):
        return can.Message.__repr__(self.__msg)

    def __str__(self):
        return can.Message.__str__(self.__msg)


class ICANGenerationStrategy(abc.ABC):
    @abc.abstractmethod
    def generate(self) -> CANMessage:
        pass


def _get_random_valid_can_message(dbc: cantools.database.Database) -> CANMessage:
    random_msg_template: cantools.database.Message = random.choice(dbc.messages)
    random_msg_signals_template = random_msg_template.signals

    random_can_msg_data = {}
    for signal_template in random_msg_signals_template:
        random_can_msg_data[signal_template.name] = random.randrange(
            math.ceil(signal_template.minimum), math.floor(signal_template.maximum)
        )

    encoded_random_can_data = random_msg_template.encode(random_can_msg_data)
    can_message = CANMessage(arbitration_id=random_msg_template.frame_id, data=encoded_random_can_data)
    return can_message


class RandomCANMessageGeneration(ICANGenerationStrategy):
    def __init__(self):
        self.__msg_pool = []
        self.__can_dbc = CONFIG.CAN_DBC_PATH

    def generate(self) -> CANMessage:
        dbc = cantools.database.load_file(CONFIG.CAN_DBC_PATH)
        can_message: CANMessage = _get_random_valid_can_message(dbc)
        return can_message


class CANMessageGenerator:
    def __init__(self, strategy: ICANGenerationStrategy):
        self.generation_strategy = strategy

    def generate(self) -> CANMessage:
        return self.generation_strategy.generate()
