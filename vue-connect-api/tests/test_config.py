from common import config


def test_get_connect_clusters(monkeypatch):
    assert config.get_connect_clusters() == [{"url": "http://localhost:8083", "id": 0}]

    monkeypatch.setenv("CONNECT_URL", "http://connect:8083")
    assert config.get_connect_clusters() == [{"url": "http://connect:8083", "id": 0}]

    monkeypatch.setenv("CONNECT_URL", "http://connect:8083//")
    assert config.get_connect_clusters() == [{"url": "http://connect:8083", "id": 0}]

    monkeypatch.setenv("CONNECT_URL", "http://connect:8083/foo/bar/")
    assert config.get_connect_clusters() == [
        {"url": "http://connect:8083/foo/bar", "id": 0}
    ]


def test_multiple_clusters(monkeypatch):

    monkeypatch.setenv("CONNECT_URL", "http://connect-a:8083;http://connect-b:8084")
    assert config.get_connect_clusters() == [
        {"url": "http://connect-a:8083", "id": 0},
        {"url": "http://connect-b:8084", "id": 1},
    ]


def test_multiple_cluster_with_names(monkeypatch):

    monkeypatch.setenv(
        "CONNECT_URL", "http://connect-a:8083,Cluster A;http://connect-b:8084,Cluster B"
    )
    assert config.get_connect_clusters() == [
        {"url": "http://connect-a:8083", "name": "Cluster A", "id": 0},
        {"url": "http://connect-b:8084", "name": "Cluster B", "id": 1},
    ]


def test_multiple_clusters_mix(monkeypatch):

    monkeypatch.setenv(
        "CONNECT_URL",
        "http://connect-a:8083,Cluster A;http://connect-b:8084;http://connect-c:8085,Cluster C",
    )
    assert config.get_connect_clusters() == [
        {"url": "http://connect-a:8083", "name": "Cluster A", "id": 0},
        {"url": "http://connect-b:8084", "id": 1},
        {"url": "http://connect-c:8085", "name": "Cluster C", "id": 2},
    ]


def test_get_db_url(monkeypatch):
    assert config.get_db_url() == "vue-connect.db"

    monkeypatch.setenv("VC_SQLITE_FILE_PATH", "/tmp/foo")
    assert config.get_db_url() == "/tmp/foo"


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
