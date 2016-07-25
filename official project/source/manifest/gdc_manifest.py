from __future__ import print_function

from manifest import Manifest
from compression import Compression


class GDCManifest(Manifest):
    headers = ["id", "filename", "md5", "size", "state"]
    separator = "\t"

    def __init__(self, filename, metadata_dict=None):
        super(self.__class__, self).__init__(filename=filename,
                                             headers=GDCManifest.headers,
                                             separator=GDCManifest.separator)

        # content contains <id_file: file_info> pairs, one record per file
        self.content = self.parse_manifest()
        # add information about entity_submitter_id if present
        if metadata_dict is not None:
            self.add_metadata_to_dict(metadata_dict)

    def get_entry_from_info(self, file_info):
        info_dict = {}
        uuid = file_info[0]
        file_name = Compression.get_filename_with_extension(
            file_info[1]).strip()

        # Special case in which the filename in the manifest is saved with the
        # uuid/file
        if "/" in file_name:
            index = file_name.index("/") + 1
            file_name = file_name[index:]

        info_dict[self.headers[1]] = file_name
        # add filename compressed if the file is compressed
        if Compression.is_file_compressed(file_info[1]):
            info_dict["name_compressed"] = file_info[1].strip()

        for i in range(2, len(self.headers)):
            info_dict[self.headers[i]] = file_info[i].strip()

        return uuid, info_dict

    def get_list_of_files(self):
        for uuid, info in self.content.viewitems():
            yield uuid, info

    def add_metadata_to_dict(self, metadata_dict):
        metadata_header = self.get_metadata_header()
        for uuid, file_info in self.content.viewitems():
            self.content[uuid][metadata_header] = metadata_dict[uuid]

    def get_name_header(self):
        return GDCManifest.headers[1]

    def get_metadata_header(self):
        return "metadata"

    def get_compressed_name(self, uuid):
        if "name_compressed" in self.content[uuid]:
            return self.content[uuid]["name_compressed"]
        else:
            return None

    def get_dir_name(self, uuid):
        filename = self.content[uuid][self.get_name_header()]
        filename = Compression.get_filename(filename)
        metadata = self.content[uuid][self.get_metadata_header()]
        dir_name = "{0}_{1}".format(metadata, filename)
        return dir_name
