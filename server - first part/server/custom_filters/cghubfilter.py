from server.filter import Filter


class CGHubFilter(Filter):
    def get_corrected_dict(self, **kwargs):
        Filter.get_corrected_dict(self, **kwargs)
