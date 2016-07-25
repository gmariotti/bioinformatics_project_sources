from __future__ import print_function

from unittest import TestCase
import utilities as utilities
import os


class TestUtilities(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_file = "__test.txt"
        cls.test_dir = "_test_temp"
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)
        with open(cls.test_file, "w") as f:
            f.write("""
            This file is an example file for,
            testing the md5 calculation.
            Let's hope it works :)
            """)
        if not os.path.exists(cls.test_dir):
            os.makedirs(cls.test_dir)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

        if os.path.exists(cls.test_dir):
            os.removedirs(cls.test_dir)

    def test_md5_file_calc(self):
        expected = "e0116ff909fdd86d27c3b44833e5066a"
        generated = utilities.md5_file_calc(TestUtilities.test_file)
        self.assertEqual(expected,
                         generated,
                         "Error, expected {0}\nreceived {1}".format(expected,
                                                                  generated))

    def test_check_valid_dir(self):
        self.assertTrue(utilities.check_valid_dir(TestUtilities.test_dir),
                        "Error, not a valid directory")
