import abc

import can

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


def _get_random_can_data() -> list:
    data = [1, 2, 5, 33, 244]
    return data


def _get_arbitration_id() -> int:
    return 155


class RandomCANMessageGeneration(ICANGenerationStrategy):
    def __init__(self):
        self.__msg_pool = []
        self.__can_dbc = CONFIG.CAN_DBC_PATH

    def generate(self) -> CANMessage:
        data = _get_random_can_data()
        arbitration_id = _get_arbitration_id()
        return CANMessage(arbitration_id=arbitration_id, data=data)


class CANMessageGenerator:
    def __init__(self, strategy: ICANGenerationStrategy):
        self.generation_strategy = strategy

    def generate(self) -> CANMessage:
        return self.generation_strategy.generate()
