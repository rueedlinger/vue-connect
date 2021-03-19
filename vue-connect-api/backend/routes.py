from datetime import datetime

import requests
from common import config, connect, store
from flask import Blueprint, g, jsonify, request
from requests.exceptions import ConnectionError, Timeout

# config
REQUEST_TIMEOUT_SEC = config.get_request_timeout()

connect_api = Blueprint("connect_api", __name__)
logger = config.get_logger("routes")


def get_store():
    cache = getattr(g, "_cache", None)
    if cache is None:
        cache = g._store = store.CacheManager(config.get_redis())

    return cache


@connect_api.teardown_request
def close_cache(exception):
    cache = getattr(g, "_cache", None)
    if cache is not None:
        cache.close()


@connect_api.route(
    "/api/cluster/<cluster_id>/connectors", strict_slashes=False, methods=["POST"]
)
def new(cluster_id):
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
            config.get_connect_url(cluster_id) + "/connectors/",
            json=cfg,
            timeout=REQUEST_TIMEOUT_SEC,
        )

        return jsonify(r.json()), r.status_code
    else:
        return jsonify({"message": "Missing configuration property 'name'."}), 400


@connect_api.route(
    "/api/cluster/<cluster_id>/connectors/<id>/config",
    strict_slashes=False,
    methods=["POST"],
)
def update(cluster_id, id):
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
        config.get_connect_url(cluster_id) + "/connectors/" + id + "/config",
        json=data,
        timeout=REQUEST_TIMEOUT_SEC,
    )

    return jsonify(r.json()), r.status_code


@connect_api.route(
    "/api/cluster/<cluster_id>/connectors/<id>/restart",
    strict_slashes=False,
    methods=["POST"],
)
def restart(cluster_id, id):
    requests.post(
        config.get_connect_url(cluster_id) + "/connectors/" + id + "/restart",
        timeout=REQUEST_TIMEOUT_SEC,
    )
    return connectors()


@connect_api.route(
    "/api/cluster/<cluster_id>/connectors/<id>/delete",
    strict_slashes=False,
    methods=["POST"],
)
def delete(cluster_id, id):
    requests.delete(
        config.get_connect_url(cluster_id) + "/connectors/" + id,
        timeout=REQUEST_TIMEOUT_SEC,
    )
    return connectors()


@connect_api.route(
    "/api/cluster/<cluster_id>/connectors/<id>/pause",
    strict_slashes=False,
    methods=["POST"],
)
def pause(cluster_id, id):
    requests.put(
        config.get_connect_url(cluster_id) + "/connectors/" + id + "/pause",
        timeout=REQUEST_TIMEOUT_SEC,
    )
    return connectors()


@connect_api.route(
    "/api/cluster/<cluster_id>/connectors/<id>/resume",
    strict_slashes=False,
    methods=["POST"],
)
def resume(cluster_id, id):
    requests.put(
        config.get_connect_url(cluster_id) + "/connectors/" + id + "/resume",
        timeout=REQUEST_TIMEOUT_SEC,
    )
    return connectors()


@connect_api.route(
    "/api/cluster/<cluster_id>/connectors/<id>/tasks/<task_id>/restart",
    strict_slashes=False,
    methods=["POST"],
)
def task_restart(cluster_id, id, task_id):
    requests.post(
        config.get_connect_url(cluster_id)
        + "/connectors/"
        + id
        + "/tasks/"
        + task_id
        + "/restart",
        timeout=REQUEST_TIMEOUT_SEC,
    )
    return connectors()


@connect_api.route("/api/cluster/<cluster_id>/config/<id>", strict_slashes=False)
def connect_config(cluster_id, id):
    r = requests.get(
        config.get_connect_url(cluster_id) + "/connectors/" + id + "/config",
        timeout=REQUEST_TIMEOUT_SEC,
    )

    return jsonify(r.json())


@connect_api.route("/api/cache", strict_slashes=False)
def polling():

    cluster_states = []
    errors = []
    resp = {"state": cluster_states, "errors": errors}

    # TODO one db call
    # load state from cache
    for cluster in config.get_connect_clusters():
        logger.info("load state from cache {}".format(cluster))
        cluster_id = cluster["id"]
        cache_entry = get_store().load(cluster_id)
        cluster_states.extend(cache_entry.get_state())
        if cache_entry.error_mesage is not None and cache_entry.running == False:
            errors.append({"message": cache_entry.error_mesage})

    return jsonify(resp)


@connect_api.route("/api/status", strict_slashes=False)
def connectors():
    cluster_states = []
    errors = []

    resp = {"state": cluster_states, "errors": errors}

    for cluster in config.get_connect_clusters():
        cluster_url = cluster["url"]
        cluster_id = cluster["id"]

        try:
            logger.info("request connect cluster state {}".format(cluster))

            state = connect.load_state(cluster_id)
            cache_entry = get_store().merge(
                store.CacheEntry(
                    id=cluster_id,
                    state=state,
                    running=True,
                    error_mesage="",
                    last_time_running=datetime.now(),
                )
            )
            cluster_states.extend(cache_entry.get_state())

        except ConnectionError:
            error_msg = config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(cluster_url)
            logger.info(error_msg)
            cache_entry = get_store().merge(
                store.CacheEntry(id=cluster_id, running=False, error_mesage=error_msg)
            )

            cluster_states.extend(cache_entry.get_state())
            errors.append({"message": error_msg})

        except Timeout:
            error_msg = config.ERROR_MSG_CLUSTER_TIMEOUT.format(cluster_url)
            logger.info(error_msg)
            get_store().merge(
                store.CacheEntry(id=cluster_id, running=False, error_mesage=error_msg)
            )
            cluster_states.extend(cache_entry.get_state())
            errors.append({"message": error_msg})
    return jsonify(resp)


@connect_api.route("/api/cluster/<cluster_id>/status/<id>", strict_slashes=False)
def status(cluster_id, id):
    r = requests.get(
        config.get_connect_url(cluster_id) + "/connectors/" + id + "/status",
        timeout=REQUEST_TIMEOUT_SEC,
    )

    return jsonify(r.json()), r.status_code


@connect_api.route(
    "/api/cluster/<cluster_id>/plugins/<name>/config/validate",
    strict_slashes=False,
    methods=["POST"],
)
def validate(cluster_id, name):
    data = request.get_json()
    if data is None:
        return (
            jsonify(
                {"message": config.ERROR_MSG_NO_DATA.format("connector configuration")}
            ),
            400,
        )

    r = requests.put(
        config.get_connect_url(cluster_id)
        + "/connector-plugins/"
        + name
        + "/config/validate",
        json=data,
        timeout=REQUEST_TIMEOUT_SEC,
    )

    return jsonify(r.json()), r.status_code


@connect_api.route("/api/plugins", strict_slashes=False)
def plugins():

    plugins = []

    for cluster in config.get_connect_clusters():
        cluster_url = cluster["url"]

        try:
            r = requests.get(
                cluster_url + "/connector-plugins", timeout=REQUEST_TIMEOUT_SEC
            )
            cluster_plugins = r.json()

            for plugin in cluster_plugins:
                plugin["name"] = plugin["class"].split(".")[-1]

                # replace string null with None
                if "version" not in plugin or plugin["version"] == "null":
                    plugin["version"] = None

            cluster["plugins"] = cluster_plugins
            plugins.append(cluster)

        except ConnectionError:
            cluster["error"] = config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(
                cluster_url
            )
            plugins.append(cluster)

        except Timeout:
            cluster["error"] = config.ERROR_MSG_CLUSTER_TIMEOUT.format(cluster_url)
            plugins.append(cluster)

    return jsonify(plugins)


@connect_api.route("/api/app/info", strict_slashes=False)
def app_info():
    app_info = {}
    app_info["vc_version"] = config.get_str_config("VC_VERSION", "dev")
    app_info["tags"] = config.get_str_config("VC_TAGS", None)
    app_info["sha"] = config.get_str_config("VC_IMAGE_GITHUB_SHA", None)
    app_info["build_time"] = config.get_str_config("VC_IMAGE_BUILD_TIME", None)

    return jsonify(app_info)


@connect_api.route("/api/cluster/info", strict_slashes=False)
def info():

    cluster_state = []

    for cluster in config.get_connect_clusters():
        cluster_url = cluster["url"]
        try:
            r = requests.get(cluster_url, timeout=REQUEST_TIMEOUT_SEC)
            cluster["info"] = r.json()
            cluster_state.append(cluster)

        except ConnectionError:
            cluster["error"] = config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(
                cluster_url
            )
            cluster_state.append(cluster)

        except Timeout:
            cluster["error"] = config.ERROR_MSG_CLUSTER_TIMEOUT.format(cluster_url)
            cluster_state.append(cluster)

    return jsonify(cluster_state)
