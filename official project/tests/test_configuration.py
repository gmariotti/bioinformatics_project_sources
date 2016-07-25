from __future__ import print_function
from unittest import TestCase

import os
from configuration import Configuration
from global_variables import CONFIGURATION_FILE


class TestConfiguration(TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists("temp"):
            os.makedirs("temp")

        if not os.path.exists("temp1"):
            os.makedirs("temp1")

    @classmethod
    def tearDownClass(cls):
        os.removedirs("temp")
        os.removedirs("temp1")
        os.remove(CONFIGURATION_FILE)

    def test_create_config_file(self):
        config = Configuration("temp")
        self.assertTrue(os.path.isfile(CONFIGURATION_FILE),
                        "{0} doesn't exist".format(CONFIGURATION_FILE))

    def test_read_config_file(self):
        if not os.path.isfile(CONFIGURATION_FILE):
            Configuration("temp")
        else:
            Configuration().update_config_file("temp")
        config = Configuration()
        self.assertEqual(config.downloadsDir,
                         "temp",
                         "Error, working dir is {0}".format(
                             config.downloadsDir))

    def test_update_config_file(self):
        config = Configuration("temp")
        config.update_config_file("temp1")
        self.assertEqual(config.downloadsDir, "temp1",
                         "Error, working dir is {0} instead of temp1".format(
                             config.downloadsDir))

    def test_remove_config_file(self):
        config = Configuration("temp")
        config.remove_config_file()
        self.assertFalse(os.path.exists(CONFIGURATION_FILE),
                         "Error, configuration file still exist")
