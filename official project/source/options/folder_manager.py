from __future__ import print_function

import logging
import os
import shutil

from compression import Compression
from configuration import Configuration
from filesize import size, alternative
from utilities import check_valid_dir, get_directories_in_dir, get_files_in_dir
from manifest.gdc_rename import GDCManifestRenamer
from manifest.custom_manifest import CustomManifest
from manifest.gdc_manifest import GDCManifest


class FoldersManager(object):
    def __init__(self, config, manifest):
        if not isinstance(manifest, CustomManifest):
            raise TypeError("manifest must be of type CustomManifest")
        if not isinstance(config, Configuration):
            raise TypeError("config must be of type Configuration")
        self.manifest = manifest
        self.config = config

    def list_folders(self):
        curr_dir = os.getcwd()

        self.folders_management()
        self.listing()

        # return to program directory
        os.chdir(curr_dir)

    def folders_management(self):
        # search for new files
        GDCManifestRenamer(self.manifest, self.config.downloadsDir).__call__()
        # check if one ore more directory have been removed manually
        self.check_folders_existence()
        self.check_previous_folders()

    def check_folders_existence(self):
        curr_dir = os.getcwd()
        os.chdir(self.config.downloadsDir)
        dir_dict, dir_key = self.manifest.get_dirname_dict()
        directories = get_directories_in_dir()
        dir_removed = False
        for key, value in dir_dict.viewitems():
            dir_name = value[dir_key]
            if dir_name not in directories:
                self.manifest.remove_uuid(value[self.manifest.headers[0]])
                message = "{0} no longer present in download directory".format(
                    dir_name)
                logging.info(message)
                dir_removed = True
        os.chdir(curr_dir)
        # serialize updated manifest
        if dir_removed:
            self.manifest.serialize_manifest()

    def check_previous_folders(self):
        curr_dir = os.getcwd()
        os.chdir(self.config.downloadsDir)
        found_old_dir = False

        directories = get_directories_in_dir()
        dir_dict, dir_key = self.manifest.get_dirname_dict()
        dir_present = [value[dir_key] for key, value in dir_dict.viewitems()]
        for directory in directories:
            # check if is not saved in the CustomManifest
            if directory not in dir_present:
                # check if a manifest is present in the directory
                files = get_files_in_dir(directory)
                manifest_list = [man for man in files
                                 if man.__contains__("manifest")]
                other_files_list = [others for others in files
                                    if not others.__contains__("manifest")]
                if len(manifest_list) > 0:
                    # there's at least a manifest, so let's try to see if the
                    # directory can be added to the list of dirs by seeing if
                    # one of the files is in the manifest
                    file_found = False
                    for manifest in manifest_list:
                        gdc_man = GDCManifest(os.path.join(directory, manifest))
                        for uuid, info in gdc_man.get_list_of_files():
                            filename = info[gdc_man.get_name_header()]
                            filename_no_ext = Compression.get_filename(filename)
                            if filename in other_files_list \
                                    and filename_no_ext in directory:
                                file_found = True
                                uuid_found = uuid
                                meta_found = directory.replace(
                                    "_" + filename_no_ext, "")
                                new_info = info
                                new_info[
                                    gdc_man.get_metadata_header()] = meta_found
                                self.manifest.add_dictionary(
                                    {uuid_found: new_info})
                                message = "Added dir {0}".format(directory)
                                logging.info(message)
                                break
                        if file_found:
                            found_old_dir = True
                            break

        os.chdir(curr_dir)
        if found_old_dir:
            self.manifest.serialize_manifest()

    def listing(self):
        curr_dir = os.getcwd()
        os.chdir(self.config.downloadsDir)
        dir_dict, dir_key = self.manifest.get_dirname_dict()
        keys = dir_dict.keys()
        for ident in keys:
            dir_name = dir_dict[ident][dir_key]
            # get list of files in the directory
            list_files = get_files_in_dir(dir_name)
            print("({0}) {1}".format(ident, dir_name))
            for value in list_files:
                if value[0] != ".":
                    size_in_bytes = os.path.getsize(
                        os.path.join(dir_name, value))
                    print(u"\t \u2514\u2501 {0}\t{1}".format(
                        value, size(size_in_bytes, alternative)))
            print("")

        os.chdir(curr_dir)
        return dir_dict, dir_key

    def remove_folder(self):
        self.folders_management()
        dir_dict, dir_key = self.listing()
        dir_to_delete = []
        not_valid = True
        while not_valid:
            selected_option = raw_input(
                "Insert IDs of folders to delete separated by space.\n>>> ")
            dir_chosen = selected_option.split()
            for directory in dir_chosen:
                try:
                    folder_id = int(directory.strip())
                except ValueError:
                    print("\nError! Insert valid IDs\n")
                    return
                except Exception:
                    return
                if 0 < folder_id <= len(dir_dict):
                    not_valid = False
                    dir_to_delete.append(folder_id)
                else:
                    break

        curr_dir = os.getcwd()
        os.chdir(self.config.downloadsDir)
        serialize_manifest = False
        for dir_id in dir_to_delete:
            uuid = dir_dict[dir_id][self.manifest.get_id_header()]
            dir_name = dir_dict[dir_id][dir_key]

            if check_valid_dir(dir_name):
                serialize_manifest = self.deleting(dir_name, uuid)
                if serialize_manifest and check_valid_dir(dir_name):
                    message = "Error, {0} still exist.".format(dir_name)
                    logging.error(message)
                else:
                    logging.info("Serialized manifest")
            else:
                message = "Error, {0} not a valid dir".format(dir_name)
                logging.warning(message)
                raise IOError

        os.chdir(curr_dir)

        if serialize_manifest:
            self.manifest.serialize_manifest()

    def deleting(self, dir_name, uuid):
        success = False
        try:
            shutil.rmtree(dir_name)
            self.manifest.remove_uuid(uuid)
            success = True
        except Exception as e:
            logging.error(e.message)
        return success
