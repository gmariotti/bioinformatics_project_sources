from __future__ import print_function

import logging
import os
import re
import shutil
import gzip
import zipfile
from utilities import check_valid_file


class Compression(object):
    pattern_compressed = re.compile(
        '(?P<filename>.*?).(?P<extension>[0-9a-zA-Z]+.[0-9a-zA-Z]+)$')

    pattern_uncompressed = re.compile(
        '(?P<filename>.*?).(?P<extension>[0-9a-zA-Z]+)$')

    @classmethod
    def uncompress_file(cls, filename):
        compression_type = cls.get_file_extension(filename)
        uncompressed_name = cls.get_filename_uncompressed(filename)
        success = False

        if check_valid_file(filename):
            message = "Current dir is: {}".format(os.getcwd())
            logging.info(message)
            if compression_type == "gz":
                message = "gzip file is {0}".format(filename)
                logging.info(message)
                with gzip.open(filename, 'rb') as f_in:
                    with open(uncompressed_name, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                        success = True
                        logging.info("gzip file success")
            elif compression_type == "zip" and zipfile.is_zipfile(filename):
                zf = zipfile.ZipFile(filename)
                try:
                    data = zf.read(uncompressed_name)
                    with open(uncompressed_name, 'wb') as f_out:
                        f_out.write(data)
                        success = True
                        logging.info("zip file success")
                except KeyError:
                    message = "ERROR: Did not find {0} in zip file".format(
                        uncompressed_name)
                    logging.warning(message)
                    return success
            else:
                message = "File '{0}' is not a valid gz/zip archive".format(
                    filename)
                logging.warning(message)
        else:
            message = "File {0} doesn't exist".format(filename)
            logging.warning(message)

        return success

    @classmethod
    def get_filename_compressed(cls, filename):
        matching = cls.pattern_compressed.match(filename)
        return matching.group('filename')

    @classmethod
    def get_filename_uncompressed(cls, filename):
        matching = cls.pattern_uncompressed.match(filename)
        return matching.group('filename')

    @classmethod
    def get_filename_with_extension(cls, filename):
        if "gz" == cls.get_file_extension(filename):
            return cls.get_filename_uncompressed(filename)
        return filename

    @classmethod
    def get_file_extension(cls, filename):
        matching = cls.pattern_uncompressed.match(filename)
        return matching.group('extension')

    @classmethod
    def get_filename(cls, filename):
        if "gz" == cls.get_file_extension(filename):
            return cls.get_filename_compressed(filename)
        else:
            return cls.get_filename_uncompressed(filename)

    @classmethod
    def is_file_compressed(cls, filename):
        result = False
        extension = cls.get_file_extension(filename)
        if extension == "gz" or extension == "zip":
            result = True
        return result
