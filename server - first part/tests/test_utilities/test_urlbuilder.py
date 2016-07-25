from unittest import TestCase
from utilities.urlbuilder import UrlQueryBuilder


class TestUrlQueryBuilder(TestCase):
    def test_url_created_with_dict(self):
        @UrlQueryBuilder(endpoint="http://test.com", path="/custom/path")
        def simple_dict_query(**kwargs):
            return kwargs

        request = simple_dict_query(key="value", query="test").prepare()
        self.assertEqual(
            "http://test.com/custom/path?query=test&key=value",
            request.url,
            "Error, found {}".format(request.url)
        )

    def test_url_escape_char(self):
        @UrlQueryBuilder(endpoint="http://test.com", path="/custom space")
        def simple_query(**kwargs):
            return kwargs

        request = simple_query(query="test").prepare()
        self.assertEqual(
            "http://test.com/custom%20space?query=test",
            request.url,
            "Error, found {}".format(request.url)
        )
