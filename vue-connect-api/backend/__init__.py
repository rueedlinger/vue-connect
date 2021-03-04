import atexit
import json
import logging
import os
import sqlite3
from sqlite3.dbapi2 import OperationalError

from apscheduler.schedulers.background import BackgroundScheduler
from common import config
from flask import Flask, jsonify
from flask_cors import CORS
from requests.exceptions import ConnectionError, Timeout
from scheduler import Scheduler, job

from backend import routes

logger = config.get_logger("server")


def handle_attribute_error(e: AttributeError):
    return (
        jsonify({"message": config.ERROR_MSG_BAD_REQUEST.format(e)}),
        400,
    )


def handle_db_error(e: OperationalError):
    logger.warn(e)
    return (
        jsonify({"message": config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(e)}),
        504,
    )


def handle_timeout_error(e: TimeoutError):
    url = config.get_cluster_from_url(e.request.url)

    return (
        jsonify({"message": config.ERROR_MSG_CLUSTER_TIMEOUT.format(url)}),
        504,
    )


def handle_connection_error(e: ConnectionError):
    url = config.get_cluster_from_url(e.request.url)

    return (
        jsonify({"message": config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(url)}),
        503,
    )


def page_not_found(e):
    return jsonify({"message": config.ERROR_MSG_NOT_FOUND}), 404


def method_not_allowed(e):
    return jsonify({"message": config.ERROR_MSG_NOT_ALLOWED}), 405


def internal_error(e):
    logger.error(e)
    return (
        jsonify({"message": config.ERROR_MSG_INTERNAL_SERVER_ERROR.format(e)}),
        500,
    )


def init_scheduler():

    # see https://stackoverflow.com/questions/14874782/apscheduler-in-flask-executes-twice
    if config.is_scheduler_activated():
        scheduler = Scheduler()
        scheduler.add_job(job.UpdateCacheJob())

        atexit.register(lambda: scheduler.shutdown())

        logger.info("starting scheduler")
        scheduler.start()


def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    console = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console.setFormatter(formatter)
    logger.addHandler(console)


def create_app():

    init_logger()

    app = Flask(__name__)
    app.register_blueprint(routes.connect_api)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # handle exceptions
    app.register_error_handler(Timeout, handle_timeout_error)
    app.register_error_handler(ConnectionError, handle_connection_error)
    app.register_error_handler(AttributeError, handle_attribute_error)
    app.register_error_handler(OperationalError, handle_db_error)

    # handler HTTP error codes
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, internal_error)

    app.before_first_request(init_scheduler)

    # should the db schema be created in the app
    create_db_scheam_in_app = bool(json.loads(os.getenv("VC_CREATE_DB_IN_APP", "true")))
    if create_db_scheam_in_app:
        logger.info("Creating DB schema in application")
        with app.app_context():
            db = sqlite3.connect(config.get_db_url())
            with app.open_resource("../schema.sql", mode="r") as f:
                db.cursor().executescript(f.read())
                db.commit()

            db.close()

    return app
