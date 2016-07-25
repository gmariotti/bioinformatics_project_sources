from controller import Controller
from jsonfiltersloader import JSONFilterLoader


class TCGAController(Controller):
    def __init__(self):
        pass

    def get_filters(self):
        return JSONFilterLoader().get_tcga_filter()

    def get_request_from_json(self, json_file):
        Controller.get_filters(self)
