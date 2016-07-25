class Controller(object):
    def get_filters(self):
        raise NotImplementedError("{} must be implemented".format(
            self.__class__.__name__))

    def get_request_from_json(self, json_file):
        raise NotImplementedError("{} must be implemented".format(
            self.__class__.__name__))