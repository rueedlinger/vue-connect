import os

DEFAULT_REST_ENDPOINT = 'http://localhost:8083'
DEFAULT_REQUEST_TIMEOUT_SEC = 5
DEFAULT_POLLING_INTERVAL_SEC = 60

ENV_POLLING_INTERVALL_CONFIG_NAME = "VC_POLLING_INTERVAL_SEC"
ENV_REQUEST_TIMEOUT_CONFIG_NAME = "VC_REQUEST_TIMEOUT_SEC"


def get_int_config(env_name, default_value):
    if os.getenv(env_name) is not None:
        try:
            return int(os.getenv(env_name))
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


def get_url():
    if os.getenv("CONNECT_URL") is not None:
        return os.getenv("CONNECT_URL").rstrip('/')
    else:
        return DEFAULT_REST_ENDPOINT


def get_request_timeout():
    return get_int_config(ENV_REQUEST_TIMEOUT_CONFIG_NAME, DEFAULT_REQUEST_TIMEOUT_SEC)


def get_poll_intervall():
    return get_int_config(ENV_POLLING_INTERVALL_CONFIG_NAME, DEFAULT_POLLING_INTERVAL_SEC)
