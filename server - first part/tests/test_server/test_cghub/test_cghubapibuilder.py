from unittest import TestCase
from server.filter import Filter
from server.cghub.cghubapibuilder import CGHubAPIBuilder


class TestCGHubAPIBuilder(TestCase):
    class TestFilter(Filter):
        def get_corrected_dict(self, **kwargs):
            corrected_dict = {}
            for key, value in kwargs.viewitems():
                if key == "query":
                    corrected_dict[key] = value

            return corrected_dict

    def test_get_url_analysis_detail(self):
        test_filter = TestCGHubAPIBuilder.TestFilter()
        api_builder = CGHubAPIBuilder(test_filter)
        request = api_builder.get_url_analysis_detail(test="test",
                                                      query="test").prepare()

        self.assertEqual(
            "{}{}?query=test".format(api_builder._endpoint,
                                     api_builder._endpointAnalysisDetail),
            request.url,
            "Error, found {}".format(request.url)
        )

    def test_get_url_analysis_full(self):
        self.fail()
