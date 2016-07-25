from __future__ import print_function

from manifest import Manifest
from utilities import check_valid_file, merge_two_dicts
from compression import Compression


class CustomManifest(Manifest):
    # Because is a "Custom" manifest, headers and separator should be passed as
    # parameters, am I right?
    def __init__(self, filename, headers, separator):
        super(self.__class__, self).__init__(
            filename=filename, headers=headers, separator=separator)

        if not check_valid_file(self.filename):
            with open(self.filename, "w") as manifest:
                line = self.separator.join(self.headers)
                manifest.write("{0}\n".format(line))

        # content contains <id_file: file_info> pairs, one record per file
        self.content = self.parse_manifest()

    def add_dictionary(self, dictionary):
        self.content = merge_two_dicts(self.content, dictionary)

    def get_entry_from_info(self, file_info):
        uuid = file_info[0]
        redux_headers = self.headers[1:]
        redux_info = file_info[1:]
        info_dict = {}
        for i in range(0, len(redux_headers)):
            info_dict[redux_headers[i]] = redux_info[i]
        return uuid, info_dict

    def get_dirname_dict(self):
        """From the content dictionary, creates a new one.
        The new key is the one represented by the header passed as a parameter.
        The value is a dictionary with uuid and an identifier from 1 to
        dictionary dimension.
        """
        dir_dict = {}
        dir_list = []
        for key, value in self.content.viewitems():
            dir_name = self.get_dir_name(key)
            dir_list.append({self.headers[0]: key, "directory": dir_name})

        def compare_dir(entry1, entry2):
            if entry1["directory"] < entry2["directory"]:
                return -1
            elif entry1["directory"] > entry2["directory"]:
                return 1
            else:
                return 0

        dir_list.sort(compare_dir)
        ident = 1
        for entry in dir_list:
            new_key = ident
            dir_dict[new_key] = entry
            ident += 1

        return dir_dict, "directory"

    def get_id_header(self):
        return self.headers[0]

    def get_name_header(self):
        return self.headers[1]

    def get_metadata_header(self):
        return self.headers[5]

    def get_dir_name(self, uuid):
        filename = self.content[uuid][self.get_name_header()]
        filename = Compression.get_filename(filename)
        metadata = self.content[uuid][self.get_metadata_header()]
        dir_name = "{0}_{1}".format(metadata, filename)
        return dir_name

    def remove_uuid(self, uuid):
        del self.content[uuid]

    def get_values(self, value):
        return value[self.headers[0]], value["id"]
