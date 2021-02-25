import logging
import time

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from common import config
from flask import Blueprint, jsonify, request
from requests.exceptions import ConnectionError, Timeout

connect_api = Blueprint("connect_api", __name__)


cache = {"loadtime": 0, "state": None, "isConnectUp": False, "message": None}

request_timeout_sec = config.get_request_timeout()
poll_intervall_sec = config.get_poll_intervall()


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
            timeout=request_timeout_sec,
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
        timeout=request_timeout_sec,
    )

    return jsonify(r.json()), r.status_code


@connect_api.route(
    "/api/connectors/<id>/restart", strict_slashes=False, methods=["POST"]
)
def restart(id):
    requests.post(
        config.get_connect_url() + "/connectors/" + id + "/restart",
        timeout=request_timeout_sec,
    )
    return connectors()


@connect_api.route(
    "/api/connectors/<id>/delete", strict_slashes=False, methods=["POST"]
)
def delete(id):
    requests.delete(
        config.get_connect_url() + "/connectors/" + id, timeout=request_timeout_sec
    )
    return connectors()


@connect_api.route("/api/connectors/<id>/pause", strict_slashes=False, methods=["POST"])
def pause(id):
    requests.put(
        config.get_connect_url() + "/connectors/" + id + "/pause",
        timeout=request_timeout_sec,
    )
    return connectors()


@connect_api.route(
    "/api/connectors/<id>/resume", strict_slashes=False, methods=["POST"]
)
def resume(id):
    requests.put(
        config.get_connect_url() + "/connectors/" + id + "/resume",
        timeout=request_timeout_sec,
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
        timeout=request_timeout_sec,
    )
    return connectors()


@connect_api.route("/api/config/<id>", strict_slashes=False)
def connect_config(id):
    r = requests.get(
        config.get_connect_url() + "/connectors/" + id + "/config",
        timeout=request_timeout_sec,
    )

    return jsonify(r.json())


@connect_api.route("/api/polling", strict_slashes=False)
def polling():
    return jsonify(cache)


@connect_api.route("/api/status", strict_slashes=False)
def connectors():
    try:
        state = load_state()
        update_cache(state)
        return jsonify(state)

    # return error and last cached result
    except ConnectionError:
        cache["message"] = config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(
            config.get_connect_url()
        )
        cache["isConnectUp"] = False

        return jsonify({"message": cache["message"], "cache": cache["state"]}), 503
    except Timeout:
        cache["message"] = config.ERROR_MSG_CLUSTER_TIMEOUT.format(
            config.get_connect_url()
        )
        cache["isConnectUp"] = False

        return (
            jsonify(
                {
                    "message": cache["message"],
                    "cache": cache["state"],
                }
            ),
            504,
        )


def load_state():
    state = []
    r = requests.get(
        config.get_connect_url() + "/connectors?expand=info&expand=status",
        timeout=request_timeout_sec,
    )
    connectors = r.json()
    for name in connectors:
        connector = connectors[name]
        connectorState = connector["status"]

        if "trace" in connectorState["connector"]:
            trace_short_connector = connectorState["connector"]["trace"].split("\n")
            if len(trace_short_connector) > 0:
                connectorState["connector"]["traceShort"] = trace_short_connector[0]

                short_task_connectors = trace_short_connector[0].split(":")

                if len(short_task_connectors) > 1:
                    connectorState["connector"][
                        "traceException"
                    ] = short_task_connectors[0].strip()
                    connectorState["connector"]["traceMessage"] = short_task_connectors[
                        1
                    ].strip()

        for task in connectorState["tasks"]:
            if "trace" in task:
                trace_short_task = task["trace"].split("\n")
                if len(trace_short_task) > 0:
                    task["traceShort"] = trace_short_task[0]

                    short_task_parts = trace_short_task[0].split(":")

                    if len(short_task_parts) > 1:
                        task["traceException"] = short_task_parts[0].strip()
                        task["traceMessage"] = short_task_parts[1].strip()

        state.append(connectorState)
    return state


@connect_api.route("/api/status/<id>", strict_slashes=False)
def status(id):
    r = requests.get(
        config.get_connect_url() + "/connectors/" + id + "/status",
        timeout=request_timeout_sec,
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
        timeout=request_timeout_sec,
    )

    return jsonify(r.json()), r.status_code


@connect_api.route("/api/plugins", strict_slashes=False)
def plugins():
    r = requests.get(
        config.get_connect_url() + "/connector-plugins", timeout=request_timeout_sec
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
    r = requests.get(config.get_connect_url(), timeout=request_timeout_sec)
    info = r.json()
    info["endpoint"] = config.get_connect_url()
    return jsonify(info)


def update_cache(state):

    cache["state"] = state
    cache["loadtime"] = time.time()
    cache["isConnectUp"] = True
    cache["message"] = None


def job_update_cache():
    logging.info("updating cache")
    try:
        state = load_state()
        update_cache(state)
    except ConnectionError:
        cache["isConnectUp"] = False
        cache["message"] = config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(
            config.get_connect_url()
        )
        logging.info(
            config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(config.get_connect_url())
        )
    except Timeout:
        cache["message"] = config.ERROR_MSG_CLUSTER_TIMEOUT.format(
            config.get_connect_url()
        )
        cache["isConnectUp"] = False
        logging.info(config.ERROR_MSG_CLUSTER_TIMEOUT.format(config.get_connect_url()))
    except Exception as e:
        cache["isConnectUp"] = False
        cache["message"] = config.ERROR_MSG_INTERNAL_SERVER_ERROR
        logging.error("Could not update cache: %s", e)


if poll_intervall_sec > 0:
    job_update_cache()
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(
        func=job_update_cache, trigger="interval", seconds=poll_intervall_sec
    )
    scheduler.start()
