from __future__ import print_function
from shutil import move

import os
import json
import re
import logging
import global_variables as gv
from compression import Compression
from utilities import check_valid_file, check_valid_dir, merge_two_dicts
from custom_manifest import CustomManifest
from gdc_manifest import GDCManifest


class GDCManifestRenamer(object):
    # Modify the upper limit in {1,4} if you want to get more info
    pattern_entity_id = re.compile(r'^(?P<entity_id>([A-Za-z0-9]+\-?){1,4})')

    def __init__(self, custom_manifest, download_dir):
        if not isinstance(custom_manifest, CustomManifest):
            raise ReferenceError(
                "Custom manifest is not of type CustomManifest")
        self.custom_manifest = custom_manifest
        self.download_dir = download_dir
        self.curr_dir = os.getcwd()
        self.cache_dir = gv.GDC_CACHE_DIR
        self.create_cache_dir()

    def __call__(self, *args, **kwargs):
        os.chdir(self.download_dir)

        manifest_list, metadata_list = self.get_file_data_lists()
        meta_dict, meta_uuid_per_file = self.get_metadata_dict(metadata_list)
        manifest_ok = []
        for manifest in manifest_list:
            gdc_manifest = GDCManifest(manifest, meta_dict)
            files_not_downloaded = []
            if not self.verify_correct_download(gdc_manifest.content,
                                                files_not_downloaded):
                message = "Error with Manifest '{0}'. It seems the download " \
                          "is not finished or some errors occurred.".format(
                    manifest)
                logging.warning(message)
                # manifest_list.remove(manifest)
                metadata_not_to_remove = self.get_metadata_not_to_remove(
                    files_not_downloaded,
                    meta_uuid_per_file)
                if metadata_not_to_remove:
                    metadata_list.remove(metadata_not_to_remove)
                continue
            else:
                manifest_ok.append(manifest)
            self.elaborate_manifest(gdc_manifest)
            self.custom_manifest.add_dictionary(gdc_manifest.content)

        self.clear_download_dir(manifest_ok, metadata_list)
        os.chdir(self.curr_dir)
        # if there's at least a manifest that has been parsed, then we can
        # serialize the custom manifest
        if len(manifest_ok) > 0:
            self.custom_manifest.serialize_manifest()

    def get_file_data_lists(self):
        files_in_curr_dir = os.listdir(".")
        manifest_list = []
        metadata_list = []

        for filename in files_in_curr_dir:
            if check_valid_file(filename):
                if "manifest" in filename:
                    manifest_list.append(filename)
                if "metadata" in filename:
                    metadata_list.append(filename)

        return manifest_list, metadata_list

    def get_metadata_dict(self, metadata_list):
        metadata_dict = dict()
        metadata_uuid_per_file = dict()
        for metadata in metadata_list:
            with open(metadata) as meta_file:
                json_data = meta_file.read()

            data = json.loads(json_data)
            uuid_per_file = list()
            # We have one dictionary per file
            for i in range(len(data)):
                info = dict(data[i])
                file_id = info['file_id']
                uuid_per_file.append(file_id)
                assoc_entities = info['associated_entities']
                assoc_len = len(assoc_entities)
                if assoc_len > 1:
                    error = "Too many associated_entities values for " \
                            "file_id '{0}'".format(file_id)
                    # print (error)

                entity_id = assoc_entities[0]['entity_submitter_id']
                # entity_id = "-".join(entity_id.split("-")[0:4])
                matching = GDCManifestRenamer.pattern_entity_id \
                    .match(entity_id)
                entity_id = matching.group('entity_id').rstrip('-')

                metadata_dict[file_id] = entity_id

            metadata_uuid_per_file[metadata] = uuid_per_file

        return metadata_dict, metadata_uuid_per_file

    def verify_correct_download(self, gdc_manifest_dict, files_not_downloaded):
        """Verify if all the files in the manifest were downloaded correctly.

        If one of the directory is missing it will return False and the current
        Manifest will not be processed.
        """
        dir_count = 0
        for uuid in gdc_manifest_dict.keys():
            if check_valid_dir(uuid):
                dir_count += 1
            else:
                files_not_downloaded.append(uuid)

        return dir_count == len(gdc_manifest_dict)

    def get_metadata_not_to_remove(self, files_uuid, uuid_per_file):
        """Compare the list of all the files (uuid) not downloaded with
        every values of the dictionary passed.
        The dictionary use has <key: value> pairs respectively the name of
        the metadata file and the list of all the file_id present in that file
        """
        for filename, uuid_list in uuid_per_file.viewitems():
            if sorted(files_uuid) == sorted(uuid_list):
                return filename

        return False

    # Works only when manifest is downloaded from gdc torrent - compressed
    # filename
    def elaborate_manifest(self, gdc_manifest):
        """From manifest information renames the directories"""
        current_dir = os.getcwd()
        name_header = gdc_manifest.get_name_header()
        for uuid, file_info in gdc_manifest.content.viewitems():
            # Dir created by gdc client
            if not check_valid_dir(uuid):
                print("Directory {0} not found".format(repr(uuid)))
                # Write something in log file because of unexpected behavior
                # The dir should be present thanks to download with torrent
                continue
            else:
                os.chdir(uuid)
                """HERE THE CORE OF RENAMING AND EXTRACTION"""
                compressed_name = gdc_manifest.get_compressed_name(uuid)
                if compressed_name is not None:
                    # Uncompress file
                    if check_valid_file(compressed_name):
                        success = Compression.uncompress_file(compressed_name)
                        if success:
                            # Remove compressed file
                            os.remove(compressed_name)
                        else:
                            logging.warning("Error uncompression")

                # Write the new small hidden manifest
                """
                 create new dictionary with the info related to the file
                 elaborated at the moment
                """
                file_dict = {uuid: file_info}
                manifest_name = ".{0}_manifest.txt".format(uuid)
                # Create the full path for new manifest file

                # TODO - change with toy GDCManifest
                content = gdc_manifest.content
                gdc_manifest.content = file_dict
                gdc_manifest.serialize_manifest(manifest_name)
                gdc_manifest.content = content

                # Go to download folder
                os.chdir(current_dir)
                # rename dir with filename
                new_dir_name = gdc_manifest.get_dir_name(uuid)
                new_dir_name = self.rename_dir(uuid, new_dir_name)

    def rename_dir(self, old_dir_name, new_dir_name):
        """Try to rename the dir with the name of the file contained.

        If the name used is already present in our downloads dir we add
        an incremental index at the end of the name.
        """
        # rename dir with filename
        rename_ok = False
        i = 1
        # We need to be sure that new_dir_name those not exist.
        while not rename_ok:
            try:
                os.rename(old_dir_name, new_dir_name)
                rename_ok = True
            except OSError:
                new_dir_name = "{0}_({1})".format(new_dir_name, i)
                logging.warning(new_dir_name)
                i += 1

        return new_dir_name  # Needed if an index has been added

    def clear_download_dir(self, manifest_list, metadata_list):
        for manifest in manifest_list:
            self.move_used_manifest(manifest)
        for metadata in metadata_list:
            self.move_used_metadata(metadata)

    def move_used_manifest(self, manifest):
        manifest_done = "done_{0}".format(manifest)
        file_src = manifest
        file_dst = os.path.join(self.cache_dir, manifest_done)
        move(file_src, file_dst)

    def move_used_metadata(self, metadata):
        metadata_done = "done_{0}".format(metadata)
        file_src = metadata
        file_dst = os.path.join(self.cache_dir, metadata_done)
        move(file_src, file_dst)

    def create_cache_dir(self):
        path = os.path.join(self.download_dir, self.cache_dir)
        if not os.path.isdir(path):
            os.mkdir(path)

    # Could be used to retrieve information from hidden manifest in each folder
    def get_manifest_list(self):
        files_in_curr_dir = os.listdir(".")
        manifest_list = []

        for filename in files_in_curr_dir:
            if check_valid_file(filename) and "manifest" in filename:
                manifest_list.append(filename)

        return manifest_list
