import os, logging
import redis

from distutils.util import strtobool

DEFAULT_REST_ENDPOINT = "http://localhost:8083"
DEFAULT_REQUEST_TIMEOUT_SEC = 5
DEFAULT_POLLING_INTERVAL_SEC = 30
DEFAULT_CACHE_TTL_SEC = 1800

DEFAULT_REDIS_HOST = "localhost"
DEFAULT_REDIS_PORT = 6379

ENV_RUN_SCHEDULER_CONFIG_NAME = "VC_RUN_SCHEDULER"
ENV_POLLING_INTERVALL_CONFIG_NAME = "VC_POLLING_INTERVAL_SEC"
ENV_REQUEST_TIMEOUT_CONFIG_NAME = "VC_REQUEST_TIMEOUT_SEC"
ENV_CACHE_TTL_CONFIG_NAME = "VC_CACHE_TTL_SEC"

ERROR_MSG_REDIS_ERROR = "Redis error. {}"
ERROR_MSG_CLUSTER_NOT_REACHABLE = "Cluster {} not reachable!"
ERROR_MSG_CLUSTER_TIMEOUT = "Request timeout cluster {} was not reachable!"
ERROR_MSG_NOT_FOUND = "Resource not found."
ERROR_MSG_NOT_ALLOWED = "The method is not allowed for this resource."
ERROR_MSG_INTERNAL_SERVER_ERROR = "Internal server error. {}"
ERROR_MSG_DB_ERROR = "DB error. {}"
ERROR_MSG_NO_DATA = "Missing data. {}."
ERROR_MSG_BAD_REQUEST = "Bad request. {}"


def get_logger(logger_name):
    return logging.getLogger("vue.connect." + logger_name)


def get_int_config(env_name, default_value):
    if os.getenv(env_name) is not None:
        try:
            return int(os.getenv(env_name))
        except ValueError:
            return default_value
    else:
        return default_value


def get_bool_config(env_name, default_value=False):
    if os.getenv(env_name) is not None:
        try:

            val = os.getenv(env_name).lower()
            return strtobool(val)

        except ValueError:
            return default_value
    else:
        return default_value


def get_str_config(env_name, default_value):
    if os.getenv(env_name) is not None:
        try:
            return os.getenv(env_name)
        except ValueError:
            return default_value
    else:
        return default_value


def get_redis():
    return redis.Redis(host=DEFAULT_REDIS_HOST, port=DEFAULT_REDIS_PORT)


def get_connect_url(cluster_id):
    try:
        for cluster in get_connect_clusters():
            if cluster["id"] == int(cluster_id):
                return cluster["url"]

        raise AttributeError("Cluster id '{}' does not exist.".format(cluster_id))
    except ValueError:
        raise AttributeError("Cluster id '{}' is not valid.".format(cluster_id))


def get_cluster_from_url(url):
    for cluster in get_connect_clusters():
        if cluster["url"] in url:
            return cluster["url"]

    raise AttributeError("Cluster for url {} does not exist.".format(url))


def get_connect_clusters():
    if os.getenv("CONNECT_URL") is not None:
        connections = []
        urls = os.getenv("CONNECT_URL").split(";")

        for id, url in enumerate(urls):
            connection = url.split(",")
            if len(connection) == 2:
                connections.append(
                    {"url": connection[0].rstrip("/"), "name": connection[1], "id": id}
                )
            else:
                connections.append({"url": connection[0].rstrip("/"), "id": id})

        return connections
    else:
        return [{"url": DEFAULT_REST_ENDPOINT, "id": 0}]


def get_cache_ttl():
    return get_int_config(ENV_CACHE_TTL_CONFIG_NAME, DEFAULT_CACHE_TTL_SEC)


def get_request_timeout():
    return get_int_config(ENV_REQUEST_TIMEOUT_CONFIG_NAME, DEFAULT_REQUEST_TIMEOUT_SEC)


def is_scheduler_activated():
    return get_bool_config(ENV_RUN_SCHEDULER_CONFIG_NAME, True)


def get_poll_intervall():
    return get_int_config(
        ENV_POLLING_INTERVALL_CONFIG_NAME, DEFAULT_POLLING_INTERVAL_SEC
    )
