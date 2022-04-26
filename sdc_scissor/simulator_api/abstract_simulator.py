import abc
import logging


class AbstractSimulator(abc.ABC):
    def __init__(self):
        """

        """
        super().__init__()

    @abc.abstractmethod
    def open(self):
        """

        """
        pass

    @abc.abstractmethod
    def close(self):
        """

        """
        pass

    @abc.abstractmethod
    def create_new_instance(self):
        """

        """
        pass

    @abc.abstractmethod
    def stop_scenario(self):
        """

        """
        pass

    @abc.abstractmethod
    def start_scenario(self):
        """

        """
        pass

    @abc.abstractmethod
    def load_scenario(self, scenario):
        """

        :param scenario:
        """
        pass

    @abc.abstractmethod
    def update_car(self):
        """

        """
        pass

    @abc.abstractmethod
    def get_car_position(self):
        """

        """
        pass


if __name__ == '__main__':
    logging.info('* abstract_simulator.py')
