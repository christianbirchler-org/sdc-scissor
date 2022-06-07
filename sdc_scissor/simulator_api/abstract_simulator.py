import abc
import logging


class AbstractSimulator(abc.ABC):
    def __init__(self):
        """ """
        super().__init__()

    @abc.abstractmethod
    def open(self):
        """
        Start the simulator in a separate process and enable interprocess communication by opening a socket.
        """
        pass

    @abc.abstractmethod
    def close(self):
        """
        Quit the simulator process and close the socket.
        """
        pass

    @abc.abstractmethod
    def create_new_instance(self):
        """
        Restart the simulator process.
        """
        pass

    @abc.abstractmethod
    def stop_scenario(self):
        """
        Stop the execution of an ongoing scenario in simulation.
        """
        pass

    @abc.abstractmethod
    def start_scenario(self):
        """
        Start the execution of a scenario in simulation.
        """
        pass

    @abc.abstractmethod
    def load_scenario(self, test, obstacles: list):
        """
        Prepare the simulator for a specific test scenario.

        :param test: An object defining the test scenario, i.e. vehicle setup, road, etc.
        :param obstacles: A list with obstacles to place in the virtual environment.
        """
        pass

    @abc.abstractmethod
    def update_car(self):
        """
        Retrieve the current sensor data of the vehicle in a running test that is executing in simulation within another process.
        """
        pass

    @abc.abstractmethod
    def get_car_position(self):
        """ """
        pass


if __name__ == "__main__":
    logging.info("* abstract_simulator.py")
