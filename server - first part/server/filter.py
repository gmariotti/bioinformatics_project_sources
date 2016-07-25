class Filter(object):
    def get_corrected_dict(self, **kwargs):
        raise NotImplementedError("{} must be implemented".format(
            self.__class__.__name__))