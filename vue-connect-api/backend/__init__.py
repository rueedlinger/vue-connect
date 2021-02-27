import logging
import sqlite3
import os
import json

from common import config
from flask import Flask, jsonify, g

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


def create_app():

    logging.basicConfig(level=logging.INFO)

    app = Flask(__name__)
    app.register_blueprint(routes.connect_api)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # handle exceptions
    app.register_error_handler(Timeout, handle_timeout_error)
    app.register_error_handler(ConnectionError, handle_connection_error)

    # handler HTTP error codes
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, internal_error)

    # should the db schema be created in the app
    create_db_scheam_in_app = bool(json.loads(os.getenv("VC_CREATE_DB_IN_APP", "true")))
    if create_db_scheam_in_app:
        logging.info("Creating DB schema in application")
        with app.app_context():
            db = sqlite3.connect(config.get_db_url())
            with app.open_resource("../schema.sql", mode="r") as f:
                db.cursor().executescript(f.read())
                db.commit()

            db.close()

    return app
