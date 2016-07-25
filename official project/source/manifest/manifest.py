from __future__ import print_function

import logging

from utilities import check_valid_file


class Manifest(object):
    def __init__(self, filename, headers, separator):
        self.filename = filename
        self.headers = headers
        self.separator = separator
        self.content = {}

    def parse_manifest(self):
        manifest_dict = {}

        with open(self.filename) as manifest:
            headers_man = self.get_headers_from_file(manifest)

            for line in manifest:
                file_info = line.rstrip("\n").split(self.separator)
                key, info_dict = self.get_entry_from_info(file_info)
                manifest_dict[key] = info_dict

        return manifest_dict

    def get_headers_from_file(self, manifest):
        line_read = manifest.readline()
        headers_man = line_read.rstrip("\r\n").split(self.separator)
        # headers_man = manifest.readline().split(self.separator)
        if headers_man != self.headers:
            logging.error("Found different headers from expected one.")
            raise ManifestError("Found different headers from expected one.")
        return headers_man

    def get_entry_from_info(self, file_info):
        """
        Defines how the information in the manifest must be handled.
        Must return (key, value) as tuple
        """
        raise NotImplementedError("Not implemented {0}".format(
            self.__class__.__name__))

    def serialize_manifest(self, filename=None, exist=False):
        manifest_filename = filename
        if filename is None:
            manifest_filename = self.filename
        if exist and check_valid_file(manifest_filename):
            raise ReferenceError("{0} already exist.".format(filename))

        with open(manifest_filename, "w") as manifest:
            headers_string = self.separator.join(self.headers)
            line_template = "{0}\n"
            manifest.write(line_template.format(headers_string))
            num_headers = len(self.headers)

            # Write information line by line. last_elem is a counter to avoid
            # printing a "\n" for the last line to write.
            last_elem = 0
            for uuid, file_info in self.content.viewitems():
                # Constructs the line
                file_line = list()
                file_line.append(str(uuid).strip())
                # We always suppose id as first element, so we start from 2nd
                for i in range(1, num_headers):
                    file_line.append(
                        str(file_info[self.headers[i]]).strip())

                line_to_write = self.separator.join(file_line)
                last_elem += 1
                if last_elem != len(self.content):
                    line_to_write = line_template.format(line_to_write)
                manifest.write(line_to_write)

        message = "Created manifest file {0} successfully.".format(
            manifest_filename)
        logging.info(message)


class ManifestError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)
