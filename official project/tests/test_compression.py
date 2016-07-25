from unittest import TestCase

import gzip
import os
import shutil
from compression import Compression


class TestCompression(TestCase):
    @classmethod
    def setUpClass(cls):
        with open("small_file.txt", "w") as small_file:
            small_file.write("Just a short string")
        with open("big_file.txt", "w") as big_file:
            line = "Just a long line with a lot of ..........................\n"
            for i in range(0, 1000):
                big_file.write(line)
        with gzip.open("_gzip_test.gz", "wb") as gzip_file:
            with open("small_file.txt", "rb") as small_file:
                shutil.copyfileobj(small_file, gzip_file)
            with open("big_file.txt", "rb") as big_file:
                shutil.copyfileobj(big_file, gzip_file)

    @classmethod
    def tearDownClass(cls):
        # Destroy everything created in setUpClass
        os.remove("small_file.txt")
        os.remove("big_file.txt")
        os.remove("_gzip_test.gz")

    def test_uncompress_file(self):
        self.fail()

    def test_get_filename_compressed(self):
        expected = "_gzip_test.txt.gz"
        actual = Compression.get_filename_compressed(expected)
        self.assertEqual(expected, actual, "Error, received {0}".format(actual))

    def test_get_filename_uncompressed(self):
        expected = "_gzip_test"
        actual = Compression.get_filename_uncompressed("_gzip_test.gz")
        self.assertEqual(expected, actual, "Error, received {0}".format(actual))

    def test_get_filename_with_extension_file_compressed(self):
        filename = "_gzip_test.txt.gz"
        actual = Compression.get_filename_with_extension(filename)
        self.assertEqual("_gzip_test.txt", actual,
                         "Error, received {0}".format(actual))

    def test_get_filename_with_extension_file_uncompressed(self):
        filename = "small_file.txt"
        actual = Compression.get_filename_with_extension(filename)
        self.assertEqual(filename, actual,
                         "Error, received {0}".format(actual))

    def test_get_file_extension(self):
        filename = "small_file.txt.gz"
        actual = Compression.get_file_extension(filename)
        self.assertEqual("gz", actual,
                         "Error, received {0}".format(actual))

    def test_get_filename_with_file_compressed(self):
        filename = "_gzip_test.txt.gz"
        actual = Compression.get_filename(filename)
        self.assertEqual("_gzip_test.txt", actual,
                         "Error, received {0}".format(actual))

    def test_get_filename_with_file_uncompressed(self):
        filename = "small_file.txt"
        actual = Compression.get_filename(filename)
        self.assertEqual(filename, actual,
                         "Error, received {0}".format(actual))

    def test_is_file_compressed(self):
        filename = "_gzip_test.txt.gz"
        self.assertTrue(Compression.is_file_compressed(filename),
                        "Error, received {0}".format(False))
