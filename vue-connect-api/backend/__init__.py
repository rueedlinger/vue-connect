import logging

from common import config
from flask import Flask, jsonify
from flask_cors import CORS
from requests.exceptions import ConnectionError, Timeout

from backend import routes


def handle_timeout_error(e):
    return (
        jsonify(
            {
                "message": config.ERROR_MSG_CLUSTER_TIMEOUT.format(
                    config.get_connect_url()
                )
            }
        ),
        504,
    )


def handle_connection_error(e):
    return (
        jsonify(
            {
                "message": config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(
                    config.get_connect_url()
                )
            }
        ),
        503,
    )


def page_not_found(e):
    return jsonify({"message": config.ERROR_MSG_NOT_FOUND}), 404


def method_not_allowed(e):
    return jsonify({"message": config.ERROR_MSG_NOT_ALLOWED}), 405


def internal_error(e):
    logging.error(e)
    return jsonify({"message": config.ERROR_MSG_INTERNAL_SERVER_ERROR}), 500


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.register_blueprint(routes.connect_api)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


# handle exceptions
app.register_error_handler(Timeout, handle_timeout_error)
app.register_error_handler(ConnectionError, handle_connection_error)

# handler HTTP error codes
app.register_error_handler(404, page_not_found)
app.register_error_handler(405, method_not_allowed)
app.register_error_handler(500, internal_error)
