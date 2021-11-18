import logging
import os
from typing import Set

from deeper.Deeper_test_generator.folders import folders
from deeper.Deeper_test_generator.ini_file import IniFile


class LogSetup:
    def __init__(self):
        self._all_loggers: Set[logging.Logger] = set()
        self._log_ini: IniFile = None

    def use_ini(self, ini_path):
        self._log_ini = IniFile(ini_path)
        log_format = self._log_ini.get_option_create_blank('config', 'format',
                                                           '[%(asctime)s %(levelname)s %(filename)s:%(lineno)d] %(message)s')
        datefmt = self._log_ini.get_option_create_blank('config', 'date_format', '%H:%M:%S')
        logging.basicConfig(format=log_format, datefmt=datefmt)
        for logger in self._all_loggers:
            self._setup_log_level(logger)

    def _setup_log_level(self, logger: logging.Logger):
        if self._log_ini:
            level = self._log_ini.get_option_create_blank('log_levels', logger.name, 'INFO')
        else:
            level = 'INFO'
        logger.setLevel(level)

    def _get_logger(self, logger_name_path):
        logger_name = os.path.basename(logger_name_path)
        log = logging.getLogger(logger_name)
        self._all_loggers.add(log)
        self._setup_log_level(log)
        return log


log_setup = LogSetup()
# IDEA: could be moved to core_lib.py/init_core()
log_setup.use_ini(folders.log_ini)


def get_logger(logger_name_path):
    return log_setup._get_logger(logger_name_path)  # pylint: disable=protected-access
