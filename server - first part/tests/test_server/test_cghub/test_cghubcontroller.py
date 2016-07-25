from unittest import TestCase
from dateutil.parser import parse
from server.filter import Filter
from server.cghub.cghubcontroller import CGHubController, CGHubAPIBuilder


class TestCGHubController(TestCase):
    class TestFilter(Filter):
        def get_corrected_dict(self, **kwargs):
            corrected_dict = {}
            if kwargs.__contains__("last_modified"):
                try:
                    parse(kwargs["last_modified"])
                    corrected_dict["last_modified"] = kwargs["last_modified"]
                except ValueError:
                    pass
                except OverflowError:
                    pass
            if kwargs.__contains__("filetype"):
                if kwargs["filetype"] == "bam" or kwargs["filetype"] == "fasta":
                    corrected_dict["filetype"] = kwargs["filetype"]

            return corrected_dict

    def test_get_filters(self):
        self.fail()

    def test_get_request_from_json(self):
        test_json_file = """{
            "analysis-details": true,
            "last_modified": "2011-07-15T23:59:59.99Z",
            "filetype": "fasta",
            "newtype": "not_valid_key"
        }
        """
        controller = CGHubController()
        controller.filter = TestCGHubController.TestFilter()
        request_test = controller.get_request_from_json(
            test_json_file).prepare()
        path_url = "{}{}".format(CGHubAPIBuilder._endpoint,
                                 CGHubAPIBuilder._endpointAnalysisDetail)
        # %3A == :
        possible_url = [
            "{}?last_modified=2011-07-15T23%3A59%3A59.99Z&filetype=fasta"
            "".format(path_url),
            "{}?filetype=fasta&last_modified=2011-07-15T23%3A59%3A59.99Z"
            "".format(path_url)
        ]
        self.assertIn(request_test.url, possible_url, "Error, found {}"
                      .format(request_test.url))
