import configparser
import logging


class IniFile:
    def __init__(self, path):
        self.path = path
        # assert isinstance(self.path, str), 'path parameter must be a string'
        self.config = configparser.ConfigParser()

    def _save(self):
        with open(self.path, 'w') as configfile:
            self.config.write(configfile)

    def _get_create_option(self, section, option, default_value):

        self.get_option(section, option, default_value)

        return self.config[section][option]

    def get_option_create_blank(self, section, option, default_value):
        val = self.get_option(section, option, None)
        if val and val != '':
            return val
        if not val:
            self.set_option(section, option, '')

        return default_value

    def set_option(self, section, option, value):
        self.check_stale()
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config[section][option] = value
        self._save()

    def get_option(self, section, option, default_value):
        self.check_stale()
        if not self.config.has_section(section) or not self.config.has_option(section, option):
            return default_value
        val = self.config[section][option]
        if val == '':
            return default_value
        return val

    def check_stale(self):
        self.config.clear()
        self.config.read(self.path)
