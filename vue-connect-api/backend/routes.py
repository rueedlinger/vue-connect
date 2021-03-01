import logging
import sqlite3
import json
from datetime import datetime

import requests
from common import config, connect, store
from flask import Blueprint, current_app, g, jsonify, request
from requests.exceptions import ConnectionError, Timeout

# config
REQUEST_TIMEOUT_SEC = config.get_request_timeout()

connect_api = Blueprint("connect_api", __name__)


def get_store():
    cache = getattr(g, "_cache", None)
    if cache is None:
        cache = g._store = store.CacheManager(config.get_db_url())

    return cache


@connect_api.teardown_request
def close_cache(exception):
    cache = getattr(g, "_cache", None)
    if cache is not None:
        cache.close()


@connect_api.route("/api/connectors", strict_slashes=False, methods=["POST"])
def new():
    data = request.get_json()
    if data is None:
        return (
            jsonify(
                {
                    "message": config.ERROR_MSG_NO_DATA.format(
                        "There was no connector configuration provided"
                    )
                }
            ),
            400,
        )

    if "name" in data:
        name = data["name"]
        del data["name"]

        cfg = {"name": name, "config": data}

        r = requests.post(
            config.get_connect_url() + "/connectors/",
            json=cfg,
            timeout=REQUEST_TIMEOUT_SEC,
        )

        return jsonify(r.json()), r.status_code
    else:
        return jsonify({"message": "Missing configuration property 'name'."}), 400


@connect_api.route(
    "/api/connectors/<id>/config", strict_slashes=False, methods=["POST"]
)
def update(id):
    data = request.get_json()

    if data is None:
        return (
            jsonify(
                {
                    "message": config.ERROR_MSG_NO_DATA.format(
                        "There is no connector configuration for '" + id + "'"
                    )
                }
            ),
            400,
        )

    r = requests.put(
        config.get_connect_url() + "/connectors/" + id + "/config",
        json=data,
        timeout=REQUEST_TIMEOUT_SEC,
    )

    return jsonify(r.json()), r.status_code


@connect_api.route(
    "/api/connectors/<id>/restart", strict_slashes=False, methods=["POST"]
)
def restart(id):
    requests.post(
        config.get_connect_url() + "/connectors/" + id + "/restart",
        timeout=REQUEST_TIMEOUT_SEC,
    )
    return connectors()


@connect_api.route(
    "/api/connectors/<id>/delete", strict_slashes=False, methods=["POST"]
)
def delete(id):
    requests.delete(
        config.get_connect_url() + "/connectors/" + id, timeout=REQUEST_TIMEOUT_SEC
    )
    return connectors()


@connect_api.route("/api/connectors/<id>/pause", strict_slashes=False, methods=["POST"])
def pause(id):
    requests.put(
        config.get_connect_url() + "/connectors/" + id + "/pause",
        timeout=REQUEST_TIMEOUT_SEC,
    )
    return connectors()


@connect_api.route(
    "/api/connectors/<id>/resume", strict_slashes=False, methods=["POST"]
)
def resume(id):
    requests.put(
        config.get_connect_url() + "/connectors/" + id + "/resume",
        timeout=REQUEST_TIMEOUT_SEC,
    )
    return connectors()


@connect_api.route(
    "/api/connectors/<id>/tasks/<task_id>/restart",
    strict_slashes=False,
    methods=["POST"],
)
def task_restart(id, task_id):
    requests.post(
        config.get_connect_url()
        + "/connectors/"
        + id
        + "/tasks/"
        + task_id
        + "/restart",
        timeout=REQUEST_TIMEOUT_SEC,
    )
    return connectors()


@connect_api.route("/api/config/<id>", strict_slashes=False)
def connect_config(id):
    r = requests.get(
        config.get_connect_url() + "/connectors/" + id + "/config",
        timeout=REQUEST_TIMEOUT_SEC,
    )

    return jsonify(r.json())


@connect_api.route("/api/polling", strict_slashes=False)
def polling():
    # load state from cache
    return jsonify(get_store().load().to_response())


@connect_api.route("/api/status", strict_slashes=False)
def connectors():
    try:
        state = connect.load_state()

        cache_entry = store.CacheEntry(
            state=state,
            running=True,
            error_mesage="",
            last_time_running=datetime.now(),
        )

        get_store().merge(cache_entry)

        return jsonify(state)

    # Connection error return last cached result
    except ConnectionError:

        cache_entry = get_store().merge(
            store.CacheEntry(
                running=False,
                error_mesage=config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(
                    config.get_connect_url()
                ),
            )
        )

        return jsonify(cache_entry.to_response()), 503

    # Timeout error return last cached result
    except Timeout:
        cache_entry = get_store().merge(
            store.CacheEntry(
                running=False,
                error_mesage=config.ERROR_MSG_CLUSTER_TIMEOUT.format(
                    config.get_connect_url()
                ),
            )
        )

        return jsonify(cache_entry.to_response()), 504


@connect_api.route("/api/status/<id>", strict_slashes=False)
def status(id):
    r = requests.get(
        config.get_connect_url() + "/connectors/" + id + "/status",
        timeout=REQUEST_TIMEOUT_SEC,
    )

    return jsonify(r.json()), r.status_code


@connect_api.route(
    "/api/plugins/<name>/config/validate", strict_slashes=False, methods=["POST"]
)
def validate(name):
    data = request.get_json()
    if data is None:
        return (
            jsonify(
                {"message": config.ERROR_MSG_NO_DATA.format("connector configuration")}
            ),
            400,
        )

    r = requests.put(
        config.get_connect_url() + "/connector-plugins/" + name + "/config/validate",
        json=data,
        timeout=REQUEST_TIMEOUT_SEC,
    )

    return jsonify(r.json()), r.status_code


@connect_api.route("/api/plugins", strict_slashes=False)
def plugins():
    r = requests.get(
        config.get_connect_url() + "/connector-plugins", timeout=REQUEST_TIMEOUT_SEC
    )
    plugins = r.json()

    for plugin in plugins:
        plugin["name"] = plugin["class"].split(".")[-1]

        # replace string null with None
        if "version" not in plugin or plugin["version"] == "null":
            plugin["version"] = None

    return jsonify(plugins)


@connect_api.route("/api/app/info", strict_slashes=False)
def app_info():
    app_info = {}
    app_info["vc_version"] = config.get_str_config("VC_VERSION", "dev")
    app_info["tags"] = config.get_str_config("VC_TAGS", None)
    app_info["sha"] = config.get_str_config("VC_IMAGE_GITHUB_SHA", None)
    app_info["build_time"] = config.get_str_config("VC_IMAGE_BUILD_TIME", None)

    return jsonify(app_info)


@connect_api.route("/api/info", strict_slashes=False)
def info():
    r = requests.get(config.get_connect_url(), timeout=REQUEST_TIMEOUT_SEC)
    info = r.json()
    info["endpoint"] = config.get_connect_url()
    return jsonify(info)
