from __future__ import print_function

import hashlib
import logging
import os

import global_variables as gv


def set_logger(level=logging.WARNING, logfile=None):
    if logfile is not None:
        logging.basicConfig(filename=logfile,
                            level=level,
                            format="[%(levelname)s - %(asctime)s] %(message)s",
                            datefmt="%Y/%m/%d_%I:%M:%S%p")
    else:
        logging.basicConfig(level=level,
                            format="[%(levelname)s - %(asctime)s] %(message)s",
                            datefmt="%Y/%m/%d_%I:%M:%S%p")


def md5_file_calc(filename):
    with open(filename, "rb") as f:
        md5 = hashlib.md5()
        block_size = md5.block_size
        buff = f.read(block_size)
        while len(buff) > 0:
            md5.update(buff)
            buff = f.read(block_size)

        return md5.hexdigest()


def check_valid_dir(directory, log=False):
    valid = True
    if not os.path.isdir(directory):
        if log:
            print(gv.DIRECTORY_INVALID.format(directory))
        valid = False

    return valid


def check_valid_file(filename, path=None, log=False):
    valid = False
    file_path = filename
    if path is not None:
        file_path = os.path.join(path, filename)
    if os.path.isfile(file_path):
        valid = True
    elif log:
        print(gv.FILE_INVALID.format(file_path))

    return valid


def get_directories_in_dir(path="."):
    return [direct for direct in os.listdir(path)
            if check_valid_dir(direct)]


def get_files_in_dir(path="."):
    return [file_found for file_found in os.listdir(path)
            if check_valid_file(file_found, path)]


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z
