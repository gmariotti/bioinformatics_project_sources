from requests import Request


class UrlQueryBuilder(object):
    """
    Used as a decorator for creation of a requests.Request object
    """

    def __init__(self, endpoint, path=None, method="GET", headers=None):
        """
        Create a requests.Request object with method, url, headers and
        parameters for the query string set.

        Neither endpoint nor path should terminate with a '/'
        :param endpoint: address to contact
        :param path: path to follow from the address. Is optional
        :param method: method to use for constructing the request. GET is
        default
        :param headers: dict of values to put in the header
        """
        if path is not None:
            url = "{}{}".format(endpoint, path)
        else:
            url = "{}".format(endpoint)

        self.url = url
        self.method = method
        self.headers = headers

    def __call__(self, func):
        def wrapped_func(*args, **kwargs):
            query_dict = func(*args, **kwargs)
            return Request(method=self.method, url=self.url,
                           headers=self.headers, params=query_dict)

        return wrapped_func
