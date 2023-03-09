import abc


class CANMessage:
    def __init__(self):
        pass


class ICANGenerationStrategy(abc.ABC):
    @abc.abstractmethod
    def generate(self) -> CANMessage:
        pass


class RandomCANGeneration(ICANGenerationStrategy):
    def generate(self) -> CANMessage:
        pass


class CANMessageGenerator:
    def __init__(self, strategy: ICANGenerationStrategy):
        self.generation_strategy = strategy

    def generate(self) -> CANMessage:
        return self.generation_strategy.generate()
