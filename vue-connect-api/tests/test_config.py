from common import config


def test_get_url(monkeypatch):
    assert config.get_connect_url() == "http://localhost:8083"

    monkeypatch.setenv("CONNECT_URL", "http://connect:8083")
    assert config.get_connect_url() == "http://connect:8083"

    monkeypatch.setenv("CONNECT_URL", "http://connect:8083//")
    assert config.get_connect_url() == "http://connect:8083"

    monkeypatch.setenv("CONNECT_URL", "http://connect:8083/foo/bar/")
    assert config.get_connect_url() == "http://connect:8083/foo/bar"


def test_get_poll_intervall(monkeypatch):
    assert config.get_poll_intervall() == 60

    monkeypatch.setenv("VC_POLLING_INTERVAL_SEC", "30")
    assert config.get_poll_intervall() == 30

    monkeypatch.setenv("VC_POLLING_INTERVAL_SEC", "FOO")
    assert config.get_poll_intervall() == 60


def test_get_request_timeout(monkeypatch):
    assert config.get_request_timeout() == 5

    monkeypatch.setenv("VC_REQUEST_TIMEOUT_SEC", "1")
    assert config.get_request_timeout() == 1

    monkeypatch.setenv("VC_REQUEST_TIMEOUT_SEC", "FOO")
    assert config.get_request_timeout() == 5


def test_get_str_config(monkeypatch):
    assert config.get_str_config("FOO", "BAR") == "BAR"

    monkeypatch.setenv("FOO", "BAZ")
    assert config.get_str_config("FOO", "BAR") == "BAZ"


def test_get_int_config(monkeypatch):
    assert config.get_int_config("FOO", 1) == 1

    monkeypatch.setenv("FOO", "100")
    assert config.get_int_config("FOO", "1") == 100
