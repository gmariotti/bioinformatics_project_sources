from server.filter import Filter
from utilities.urlbuilder import UrlQueryBuilder


class CGHubAPIBuilder(object):
    _endpoint = "https://cghub.ucsc.edu"
    _endpointAnalysisDetail = "/cghub/metadata/analysisDetail"
    _endpointAnalysisFull = "/cghub/metadata/analysisFull"
    _headers = {"Accept": "application/json"}

    def __init__(self, filter_obj):
        """
        filter_obj must be a subclass of Filter.
        :param filter_obj: corrector of the query dictionary
        """
        if not isinstance(filter_obj, Filter):
            raise TypeError("filterObj is not of type Filter")
        self.filterObj = filter_obj

    @UrlQueryBuilder(
        endpoint=_endpoint, path=_endpointAnalysisDetail, headers=_headers)
    def get_url_analysis_detail(self, **kwargs):
        query_dict = self.filterObj.get_corrected_dict(**kwargs)
        return query_dict

    @UrlQueryBuilder(
        endpoint=_endpoint, path=_endpointAnalysisFull, headers=_headers)
    def get_url_analysis_full(self, **kwargs):
        query_dict = self.filterObj.get_corrected_dict(**kwargs)
        return query_dict
