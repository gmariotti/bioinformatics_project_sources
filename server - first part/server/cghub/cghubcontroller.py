import json
from controller import Controller
from jsonfiltersloader import JSONFilterLoader
from custom_filters.cghubfilter import CGHubFilter
from .cghubapibuilder import CGHubAPIBuilder


class CGHubController(Controller):
    def __init__(self):
        self.filter = CGHubFilter()
        pass

    def get_filters(self):
        return JSONFilterLoader().get_cghub_filter()

    def get_request_from_json(self, json_file):
        json_dict = json.loads(json_file)
        builder = CGHubAPIBuilder(self.filter)
        if self.is_analysis_detail(json_dict):
            request = builder.get_url_analysis_detail(**json_dict)
        else:
            request = builder.get_url_analysis_full(**json_dict)
        return request

    @classmethod
    def is_analysis_detail(cls, json_dict):
        return json_dict['analysis-details']
