from __future__ import print_function

import logging

import global_variables as gv
from configuration import Configuration, ConfigurationError
from menu import Menu, Option
from terminal import read_terminal_arguments
from manifest.custom_manifest import CustomManifest
from manifest.gdc_manifest import GDCManifest
from options.exit import Exit, ExitError
from options.folder_manager import FoldersManager
from utilities import set_logger


def get_options_list(config_obj, custom_manifest):
    manager = FoldersManager(config_obj, custom_manifest)
    list_opt = Option(gv.LIST_TITLE, gv.LIST_COMMENT,
                      manager.list_folders)
    delete_opt = Option(gv.DELETE_DIR_TITLE, gv.DELETE_DIR_COMMENT,
                        manager.remove_folder)
    update_conf_opt = Option(gv.UPDATE_TITLE, gv.UPDATE_COMMENT,
                             config_obj.callable_update)
    remove_conf_opt = Option(gv.REMOVE_TITLE, gv.REMOVE_COMMENT,
                             config_obj.callable_remove)
    exit_opt = Option(gv.EXIT_TITLE, gv.EXIT_COMMENT,
                      Exit.default_exit())
    return [list_opt, delete_opt, update_conf_opt, remove_conf_opt, exit_opt]


if __name__ == "__main__":
    read_terminal_arguments()
    set_logger()

    exitProgram = False
    # run configuration management
    config = Configuration()
    manifest = CustomManifest(
        gv.MANIFEST_FILE, gv.MANIFEST_HEADERS, gv.MANIFEST_SEPARATOR)
    menu = Menu(gv.MENU_TITLE)

    options = get_options_list(config, manifest)
    menu.add_options(*options)
    menu.show()
    while not exitProgram:
        try:
            menu.select_option()
        except ExitError as e:
            logging.info(e.message)
            exitProgram = True
        except ConfigurationError as e:
            print(e.message)
            config = Configuration()
            manifest = CustomManifest(
                gv.MANIFEST_FILE, gv.MANIFEST_HEADERS, GDCManifest.separator)
            menu.reset_options()
            options = get_options_list(config, manifest)
            menu.add_options(*options)
            print("")

    exit(0)
