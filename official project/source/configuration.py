from __future__ import print_function

import logging
import os
import global_variables as gv
from ConfigParser import ConfigParser  # 2to3 for conversion
from utilities import check_valid_file, check_valid_dir


class Configuration(object):
    def __init__(self, download_dir=None):
        self.filename = gv.CONFIGURATION_FILE
        self.downloadsDir = None

        # Ask the user for the directory if the configuration file doesn't
        # exist or read it from the file
        if not check_valid_file(gv.CONFIGURATION_FILE):
            if download_dir is None:
                download_dir = self.read_download_dir()
            self.create_config_file(self.filename, download_dir)
        else:
            self.read_config_file(self.filename)

    @classmethod
    def check_configuration_existence(cls):
        exist = False
        if check_valid_file(gv.CONFIGURATION_FILE):
            exist = True
        return exist

    def create_config_file(self, filename, download_dir):
        self.downloadsDir = download_dir
        parser = ConfigParser()
        parser.add_section(gv.GDC_SECTION)
        parser.set(gv.GDC_SECTION, gv.GDC_DOWNLOAD_DIR, self.downloadsDir)

        with open(filename, "w") as conf_file:
            parser.write(conf_file)

        print(gv.CONFIGURATION_SUCCESS.format(self.downloadsDir))
        message = gv.DIRECTORY_MESSAGE.format(self.downloadsDir)
        logging.info(message)

    def read_download_dir(self):
        print(gv.DIR_REQUEST)
        download_dir = str(raw_input(gv.PYTHON_INPUT))
        while not check_valid_dir(download_dir):
            print(gv.DIRECTORY_INVALID.format(download_dir))
            print(gv.DIR_REQUEST)
            download_dir = str(raw_input(gv.PYTHON_INPUT))
        return download_dir

    def read_config_file(self, filename):
        parser = ConfigParser()
        parser.read(filename)
        self.downloadsDir = parser.get(gv.GDC_SECTION, gv.GDC_DOWNLOAD_DIR)
        if self.downloadsDir is None:
            raise ValueError(gv.DIRECTORY_ERROR)

    def update_config_file(self, download_dir):
        if not check_valid_dir(download_dir):
            message = gv.DIRECTORY_INVALID.format(download_dir)
            logging.error(message)
            raise ValueError(message)
        if check_valid_file(self.filename):
            parser = ConfigParser()
            parser.read(self.filename)
            parser.set(gv.GDC_SECTION, gv.GDC_DOWNLOAD_DIR, download_dir)
            with open(self.filename, "w") as conf_file:
                parser.write(conf_file)
            self.read_config_file(self.filename)
        else:
            self.create_config_file(self.filename, download_dir)

    def remove_config_file(self):
        removed = False
        if check_valid_file(self.filename):
            try:
                os.remove(self.filename)
                removed = True
            except OSError as e:
                logging.error(e.message)
        return removed

    def callable_update(self):
        download_dir = self.read_download_dir()
        self.update_config_file(download_dir)
        message = "UpdateConfig with dir {0}".format(self.downloadsDir)
        logging.info(message)
        print(gv.UPDATE_SUCCESS.format(self.downloadsDir))

    def callable_remove(self):
        self.remove_config_file()
        logging.info("RemoveConfig")
        raise ConfigurationError("Missing configuration. New one to construct")


class ConfigurationError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)
