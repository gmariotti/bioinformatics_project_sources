import json

from pysistence import make_dict
from utilities.singleton import Singleton


# TODO - still missing the possibility to update the dict with a new
# TODO - version of them
class JSONFilterLoader(object):
    __metaclass__ = Singleton

    def __init__(self):
        # TODO - load TCGA json filter and CGHub json filter
        tcga_dict = json.load("tcga-json")
        cghub_dict = json.load("cghub-json")
        # make corresponding dict immutable
        self.__tcga_filter = make_dict(**tcga_dict)
        self.__cghub_filter = make_dict(**cghub_dict)
        # TODO extract the last modification time from the dict
        self.__tcga_last_mod_time = None
        self.__cghub_last_mod_time = None

    def get_tcga_filter(self):
        return self.__tcga_filter

    def get_cghub_filter(self):
        return self.__cghub_filter

    def get_tcga_last_mod_time(self):
        return self.__tcga_last_mod_time

    def get_cghub_last_mod_time(self):
        return self.__cghub_last_mod_time
