CONFIGURATION_FILE = "configuration.ini"
GDC_SECTION = "gdc_data_section"
GDC_DOWNLOAD_DIR = "config"
GDC_CACHE_MANIFEST = "cache_manifest"
GDC_CACHE_DIR = ".cache_gdc"

# Constant for program manifest
MANIFEST_FILE = "MANIFEST.txt"
MANIFEST_HEADERS = ["id", "filename", "md5", "size", "state", "metadata"]
MANIFEST_SEPARATOR = "\t"

# Menu strings
MENU_TITLE = "=== GDC Management ==="
LIST_TITLE = "List of downloaded files"
LIST_COMMENT = "Prints the list of folders and downloaded files in the " \
               "directory submitted during configuration."
DELETE_DIR_TITLE = "Delete a directory"
DELETE_DIR_COMMENT = "Deletes a directory in the download one, based on user " \
                     "input"
UPDATE_TITLE = "Update configuration"
UPDATE_COMMENT = "Updates the directory in the configuration file, " \
                 "with the one passed."
REMOVE_TITLE = "Remove configuration"
REMOVE_COMMENT = "Removes the configuration file."
SCAN_COMMENT = "Scans the download directory for renaming new downloaded files."
EXIT_TITLE = "Exit"
EXIT_COMMENT = "Ends the program."
CREATE_COMMENT = "Creates a configuration file with the passed directory."
LOGGING_INFO = "Prints also the logging information at info level."
LOGGING_FILE = "Sets a file where to write the log."

# Input requests - EN
DIR_REQUEST = "Insert directory path where files are placed."
CACHE_REQUEST = "Do you want to keep a copy of the downloaded manifest? [Y/N]"
PYTHON_INPUT = ">>> "

# Various messages
CONFIGURATION_SUCCESS = "Configuration file has been created with directory {0}"
UPDATE_SUCCESS = "New download directory is {0}"
DIRECTORY_MESSAGE = "Directory is {0}"
DIRECTORY_INVALID = "{0} is not a valid directory."
DIRECTORY_ERROR = "Directory is not present, even if the file has been created."
FILE_INVALID = "{0} is not a valid file."
