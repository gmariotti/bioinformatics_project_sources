import requests as Requests
from flask import Flask, Response, request
from .jsonfiltersloader import JSONFilterLoader
from .tcga.tcgacontroller import TCGAController
from .cghub.cghubcontroller import CGHubController

app = Flask(__name__)


@app.route("/")
def get_filters():
    """
    Get the list of filters available for the different services
    offered by the web service

    :return:
    """
    pass


@app.route("/lastmodification")
def get_filters_last_modification_time():
    lastmodtime_tcga = JSONFilterLoader().get_tcga_last_mod_time()
    lastmodtime_cghub = JSONFilterLoader.get_cghub_last_mod_time()

    # TODO - format response accordingly

    return


@app.route("/tcga/filter")
def get_tcga_filter():
    """
    Get the list of filters available from the TCGADataMatrix.
    By default, the list of filters is in json

    :return:
    """
    filters = TCGAController().get_filters()
    resp = Response(
        response=filters,
        status=200,
        mimetype="application/json"
    )
    return resp


@app.route("/tcga/filter/lastmodification")
def get_tcga_filter_last_modification_time():
    lastmodtime = JSONFilterLoader().get_tcga_last_mod_time()
    # TODO - format response accordingly
    return


@app.route("/cghub/filter")
def get_cghub_filter():
    """
    Get the list of filters available from CGHub

    :return:
    """
    controller = CGHubController()
    json_filters = controller.get_filters()

    # TODO -> prepare response to return
    resp = Response(
        response=json_filters,
        status=200,
        mimetype="application/json"
    )

    return resp


@app.route("/cghub/filter/lastmodification")
def get_cghub_filter_last_modification_time():
    lastmodtime = JSONFilterLoader().get_cghub_last_mod_time()
    # TODO - format response accordingly
    return


@app.route("/cghub/requestinfo", methods=["POST"])
def get_cghub_data_from_filters():
    try:
        # request must have mimetype "application/json" to be valid
        if request.is_json:
            controller = CGHubController()
            cghub_request = controller.get_request_from_json(request.get_json())

            response = Requests.session().send(cghub_request.prepare())
            if response.status_code == request.codes.ok:
                # forward the reply to the client
                return None
            else:
                # TODO - notify client of error in response
                raise Exception
        else:  # TODO - error handling
            raise Exception
    except Exception:
        # TODO - handle exception
        # consider handling an exception at each else error in order to
        # returning here the right response
        return


if __name__ == "__main__":
    # initialize filters for TCGA and CGHub before loading the server
    JSONFilterLoader()
    app.run()
