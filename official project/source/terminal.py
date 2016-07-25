from __future__ import print_function

import argparse  # pip install argparse for python 2.6
import logging

import global_variables as gv

from configuration import Configuration
from utilities import check_valid_dir, set_logger
from manifest.custom_manifest import CustomManifest
from manifest.gdc_manifest import GDCManifest
from manifest.gdc_rename import GDCManifestRenamer
from options.folder_manager import FoldersManager


def read_terminal_arguments():
    parser = create_parser()
    args = parser.parse_args()

    # if True, it means the program is not used in the command line version
    if is_empty(args):
        set_logger()
        return
    else:
        config = None
        exit_program = False

        # logging options
        level = logging.WARNING
        logfile = None
        if args.verbose:
            level = logging.INFO
        if args.log_file is not None:
            logfile = args.log_file
        set_logger(level, logfile)

        # -c and -u are mutually exclusive options
        # check -c option
        if args.create is not None:
            if check_valid_dir(args.create):
                if Configuration.check_configuration_existence():
                    print("Configuration file already exist.")
                    print("Use -u to update the directory")
                    exit(-1)
                config = Configuration(args.create)
                exit_program = True
            else:
                print(gv.DIRECTORY_INVALID.format(args.update))
                exit(-1)
        elif args.update is not None:  # check -u option
            if check_valid_dir(args.update):
                if not Configuration.check_configuration_existence():
                    print("Use option -c for creating a configuration file")
                    exit(-1)
                config = Configuration()
                config.update_config_file(args.update)
                exit_program = True
            else:
                print(gv.DIRECTORY_INVALID.format(args.update))
                exit(-1)

        if config is None:  # neither -c nor -u have been used
            config = Configuration()

        # -r, -l and -s are mutually exclusive options
        if args.listing:
            FoldersManager(
                config,
                CustomManifest(gv.MANIFEST_FILE,
                               gv.MANIFEST_HEADERS,
                               GDCManifest.separator)
            ).list_folders()
            exit(0)
        elif args.remove_config:
            success = config.remove_config_file()
            if success:
                print("Configuration file correctly removed")
            else:
                print("Configuration file not found")
            exit(0)
        elif args.scan:
            GDCManifestRenamer(
                CustomManifest(gv.MANIFEST_FILE,
                               gv.MANIFEST_HEADERS,
                               GDCManifest.separator),
                config.downloadsDir
            ).__call__()
            exit(0)

        # exits from the program only if -c or -u have been used but -r,
        # -l and -s are not.
        if exit_program:
            exit(0)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true",
                        help=gv.LOGGING_INFO)
    parser.add_argument("--log-file", metavar="file",
                        help=gv.LOGGING_FILE)

    group_1 = parser.add_mutually_exclusive_group()
    group_1.add_argument("-l", "--listing", action="store_true",
                         help=gv.LIST_COMMENT)
    group_1.add_argument("-rc", "--remove-config", action="store_true",
                         help=gv.REMOVE_COMMENT)
    group_1.add_argument("-s", "--scan", action="store_true",
                         help=gv.SCAN_COMMENT)
    group_2 = parser.add_mutually_exclusive_group()
    group_2.add_argument("-u", "--update", metavar="dir",
                         help=gv.UPDATE_COMMENT)
    group_2.add_argument("-c", "--create", metavar="dir",
                         help=gv.CREATE_COMMENT)
    return parser


def is_empty(args):
    result = False
    if not args.listing and not args.remove_config and not args.scan \
            and not args.verbose and args.log_file is None \
            and args.update is None and args.create is None:
        result = True

    return result
