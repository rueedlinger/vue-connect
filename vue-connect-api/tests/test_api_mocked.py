import json
from unittest.mock import patch

import backend
import pytest

from tests import MockResp

TIMEOUT = 5


@pytest.fixture
def client(monkeypatch):

    # disable scheduler
    monkeypatch.setenv("VC_RUN_SCHEDULER", "false")

    app = backend.create_app()

    with app.test_client() as client:
        yield client


def test_status_empty(client):

    patcher = patch("requests.get")
    mock_get = patcher.start()
    mock_get.return_value = MockResp(data=[])

    resp = client.get("/api/status")
    patcher.stop()

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert 200 == resp.status_code
    assert b"[]" in resp.data


def test_status_with_data(client):

    data = {
        "foo": {
            "info": {},
            "status": {"name": "foo", "connector": {"state": "RUNNING"}, "tasks": []},
        }
    }
    patcher = patch("requests.get")
    mock_get = patcher.start()
    mock_get.return_value = MockResp(data=data)

    resp = client.get("/api/status")
    patcher.stop()

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert 200 == resp.status_code
    assert (
        b'{"errors":[],"state":[{"cluster":{"id":0,"url":"http://localhost:8083"},"connector":{"state":"RUNNING"},"name":"foo","tasks":[]}]}'
        in resp.data
    )


def test_status_with_id(client):

    status = {"foo": "bar"}

    patcher = patch("requests.get")
    mock_get = patcher.start()
    mock_get.return_value = MockResp(data=status)

    resp = client.get("/api/cluster/0/status/foo")
    patcher.stop()

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors/foo/status", timeout=TIMEOUT
    )

    assert 200 == resp.status_code
    assert b'{"foo":"bar"}' in resp.data


def test_new_missing_data(client):

    patcher = patch("requests.post")
    mock_post = patcher.start()
    mock_post.return_value = MockResp()

    resp = client.post("/api/cluster/0/connectors")
    patcher.stop()

    mock_post.assert_not_called()
    assert 400 == resp.status_code
    assert (
        b'{"message":"Missing data. There was no connector configuration provided."}'
        in resp.data
    )


def test_new_missing_name_attribute(client):

    data = {"config": {"bar": "123"}}

    patcher = patch("requests.post")
    mock_post = patcher.start()
    mock_post.return_value = MockResp()

    resp = client.post(
        "/api/cluster/0/connectors",
        data=json.dumps(data),
        content_type="application/json",
    )
    patcher.stop()

    mock_post.assert_not_called()

    assert 400 == resp.status_code
    assert b'{"message":"Missing configuration property \'name\'."}' in resp.data


def test_new(client):

    data = {"name": "foo", "bar": "123", "baz": "abc"}
    expected = {"name": "foo", "config": {"bar": "123", "baz": "abc"}}

    patcher = patch("requests.post")
    mock_post = patcher.start()
    mock_post.return_value = MockResp(data={"foo": "bar"})

    resp = client.post(
        "/api/cluster/0/connectors",
        data=json.dumps(data),
        content_type="application/json",
    )
    patcher.stop()

    mock_post.assert_called_once_with(
        "http://localhost:8083/connectors/", json=expected, timeout=TIMEOUT
    )

    assert 200 == resp.status_code
    assert b'{"foo":"bar"}' in resp.data


def test_update(client):

    data = {"name": "foo", "bar": "123", "baz": "abc"}

    patcher = patch("requests.put")
    mock_put = patcher.start()
    mock_put.return_value = MockResp(data={"foo": "bar"})

    resp = client.post(
        "/api/cluster/0/connectors/foo/config",
        data=json.dumps(data),
        content_type="application/json",
    )
    patcher.stop()

    mock_put.assert_called_once_with(
        "http://localhost:8083/connectors/foo/config", json=data, timeout=TIMEOUT
    )

    assert 200 == resp.status_code
    assert b'{"foo":"bar"}' in resp.data


def test_update_missing_data(client):

    patcher = patch("requests.put")
    mock_put = patcher.start()
    mock_put.return_value = MockResp()

    resp = client.post("/api/cluster/0/connectors/foo/config")
    patcher.stop()

    mock_put.assert_not_called()

    assert (
        b'{"message":"Missing data. There is no connector configuration for \'foo\'."}'
        in resp.data
    )
    assert 400 == resp.status_code


def test_restart(client):

    patcherPost = patch("requests.post")
    mock_post = patcherPost.start()
    mock_post.return_value = MockResp()

    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(
        data={"foo": {"name": {}, "status": {"connector": {}, "tasks": []}}}
    )

    resp = client.post("/api/cluster/0/connectors/foo/restart")
    patcherPost.stop()
    patcherGet.stop()

    mock_post.assert_called_once_with(
        "http://localhost:8083/connectors/foo/restart", timeout=TIMEOUT
    )

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert 200 == resp.status_code
    assert (
        b'{"errors":[],"state":[{"cluster":{"id":0,"url":"http://localhost:8083"},"connector":{},"tasks":[]}]}'
        in resp.data
    )


def test_task_restart(client):

    patcherPost = patch("requests.post")
    mock_post = patcherPost.start()
    mock_post.return_value = MockResp()

    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(
        data={"foo": {"name": {}, "status": {"connector": {}, "tasks": []}}}
    )

    resp = client.post("/api/cluster/0/connectors/foo/tasks/0/restart")
    patcherPost.stop()
    patcherGet.stop()

    mock_post.assert_called_once_with(
        "http://localhost:8083/connectors/foo/tasks/0/restart", timeout=TIMEOUT
    )

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert 200 == resp.status_code
    assert (
        b'{"errors":[],"state":[{"cluster":{"id":0,"url":"http://localhost:8083"},"connector":{},"tasks":[]}]}'
        in resp.data
    )


def test_delete(client):

    patcherDelete = patch("requests.delete")
    mock_delete = patcherDelete.start()
    mock_delete.return_value = MockResp()

    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(
        data={"foo": {"name": {}, "status": {"connector": {}, "tasks": []}}}
    )

    resp = client.post("/api/cluster/0/connectors/foo/delete")
    patcherDelete.stop()
    patcherGet.stop()

    mock_delete.assert_called_once_with(
        "http://localhost:8083/connectors/foo", timeout=TIMEOUT
    )

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert 200 == resp.status_code
    assert (
        b'{"errors":[],"state":[{"cluster":{"id":0,"url":"http://localhost:8083"},"connector":{},"tasks":[]}]}'
        in resp.data
    )


def test_pause(client):

    patcherPut = patch("requests.put")
    mock_put = patcherPut.start()
    mock_put.return_value = MockResp()

    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(
        data={"foo": {"name": {}, "status": {"connector": {}, "tasks": []}}}
    )

    resp = client.post("/api/cluster/0/connectors/foo/pause")
    patcherPut.stop()
    patcherGet.stop()

    mock_put.assert_called_once_with(
        "http://localhost:8083/connectors/foo/pause", timeout=TIMEOUT
    )

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert 200 == resp.status_code
    assert (
        b'{"errors":[],"state":[{"cluster":{"id":0,"url":"http://localhost:8083"},"connector":{},"tasks":[]}]}'
        in resp.data
    )


def test_resume(client):

    patcherPut = patch("requests.put")
    mock_put = patcherPut.start()
    mock_put.return_value = MockResp()

    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(
        data={"foo": {"name": {}, "status": {"connector": {}, "tasks": []}}}
    )

    resp = client.post("/api/cluster/0/connectors/foo/resume")
    patcherPut.stop()
    patcherGet.stop()

    mock_put.assert_called_once_with(
        "http://localhost:8083/connectors/foo/resume", timeout=TIMEOUT
    )

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert 200 == resp.status_code
    assert (
        b'{"errors":[],"state":[{"cluster":{"id":0,"url":"http://localhost:8083"},"connector":{},"tasks":[]}]}'
        in resp.data
    )


def test_polling(client):
    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp()

    resp = client.get("/api/cache")
    patcherGet.stop()

    mock_get.assert_not_called()

    assert 200 == resp.status_code
    assert b'{"errors":[],"state":[]' in resp.data


def test_config(client):
    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(data={"foo": "bar"})

    resp = client.get("/api/cluster/0/config/foo")
    patcherGet.stop()

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors/foo/config", timeout=TIMEOUT
    )

    assert 200 == resp.status_code
    assert b'{"foo":"bar"}' in resp.data


def test_plugins(client):
    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(data=[{"class": "foo.bar"}])

    resp = client.get("/api/plugins")
    patcherGet.stop()

    mock_get.assert_called_once_with(
        "http://localhost:8083/connector-plugins", timeout=TIMEOUT
    )

    assert 200 == resp.status_code
    assert b'[{"class":"foo.bar","name":"bar","version":null}]' in resp.data


def test_validate(client):

    data = {"foo": "bar"}

    patcherPut = patch("requests.put")
    mock_put = patcherPut.start()
    mock_put.return_value = MockResp(data={"class": "foo.bar"})

    resp = client.post(
        "/api/cluster/0/plugins/foo/config/validate",
        data=json.dumps(data),
        content_type="application/json",
    )
    patcherPut.stop()

    mock_put.assert_called_once_with(
        "http://localhost:8083/connector-plugins/foo/config/validate",
        json=data,
        timeout=TIMEOUT,
    )

    assert 200 == resp.status_code
    assert b'{"class":"foo.bar"}' in resp.data


def test_app_info(client):

    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp()

    resp = client.get("/api/app/info")
    patcherGet.stop()

    mock_get.assert_not_called()

    assert 200 == resp.status_code
    assert b'{"build_time":null,"sha":null,"tags":null,"vc_version":"dev"}' in resp.data


def test_cluster_info(client):

    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(data={"foo": "bar"})

    resp = client.get("/api/cluster/info")
    patcherGet.stop()

    mock_get.assert_called_once_with("http://localhost:8083", timeout=TIMEOUT)

    assert 200 == resp.status_code
    assert b'[{"id":0,"info":{"foo":"bar"},"url":"http://localhost:8083"}]' in resp.data


def test_multi_cluster_call(client, monkeypatch):
    monkeypatch.setenv("CONNECT_URL", "http://foo:1234;http://bar:1234")

    data = {
        "foo": {
            "info": {},
            "status": {"name": "foo", "connector": {"state": "RUNNING"}, "tasks": []},
        }
    }
    patcher = patch("requests.get")
    mock_get = patcher.start()
    mock_get.return_value = MockResp(data=data)

    resp = client.get("/api/status")
    patcher.stop()

    assert mock_get.call_count == 2

    assert 200 == resp.status_code
