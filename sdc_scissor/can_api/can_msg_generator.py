import abc


class ICANGenerationStrategy(abc.ABC):
    @abc.abstractmethod
    def generate(self):
        pass


class RandomCANGeneration(ICANGenerationStrategy):
    def generate(self):
        pass


class CANMessageGenerator:
    def __init__(self, strategy: ICANGenerationStrategy):
        self.generation_strategy = strategy

    def generate(self):
        self.generation_strategy.generate()
