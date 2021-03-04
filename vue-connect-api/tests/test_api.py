import json

import pytest
import backend

path_get_for_cluster = [
    "/api/cluster/0/status/foo",
    "/api/cluster/0/config/foo",
]

path_get_for_all = [
    "/api/plugins",
    "/api/status/",
]


path_post_for_cluster = [
    "/api/cluster/0/connectors/foo/tasks/0/restart",
    "/api/cluster/0/connectors/foo/resume",
    "/api/cluster/0/connectors/foo/pause",
    "/api/cluster/0/connectors/foo/delete",
    "/api/cluster/0/connectors/foo/restart",
]


@pytest.fixture
def client(monkeypatch):

    # disable scheduler
    monkeypatch.setenv("VC_RUN_SCHEDULER", "false")
    monkeypatch.setenv("CONNECT_URL", "http://foo:1234")

    app = backend.create_app()

    with app.test_client() as client:
        yield client


def test_api_not_found(client):
    resp = client.get("/foo")
    assert b'{"message":"Resource not found."}' in resp.data
    assert 404 == resp.status_code


def test_api_not_allowed(client):
    resp = client.post(
        "/api/status", data=json.dumps({}), content_type="application/json"
    )
    assert b'{"message":"The method is not allowed for this resource."}' in resp.data
    assert 405 == resp.status_code


def test_api_missing_data_with_post(client):
    resp = client.post("/api/cluster/0/connectors/foo/config")
    assert (
        b'{"message":"Missing data. There is no connector configuration for \'foo\'."}'
        in resp.data
    )
    assert 400 == resp.status_code

    resp = client.post("/api/cluster/0/connectors")
    assert (
        b'{"message":"Missing data. There was no connector configuration provided."}'
        in resp.data
    )
    assert 400 == resp.status_code


def test_api_post_with_data(client):
    resp = client.post(
        "/api/cluster/0/connectors/foo/config",
        data=json.dumps({}),
        content_type="application/json",
    )
    assertNotReachable(resp)

    resp = client.post(
        "/api/cluster/0/connectors",
        data=json.dumps({"name": "foo"}),
        content_type="application/json",
    )
    assertNotReachable(resp)

    resp = client.post(
        "/api/cluster/0/connectors",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert b'{"message":"Missing configuration property \'name\'."}' in resp.data
    assert 400 == resp.status_code


def test_api_invalid_cluster(client):
    resp = client.get("/api/cluster/1/status/foo")
    assert b'{"message":"Bad request. Cluster id \'1\' does not exist."}' in resp.data
    assert 400 == resp.status_code

    resp = client.get("/api/cluster/hello/status/foo")
    assert b'{"message":"Bad request. Cluster id \'hello\' is not valid."}' in resp.data
    assert 400 == resp.status_code


def test_api_cache(client):
    resp = client.get("/api/cache")
    assert b'{"errors":[],"state":[]}' in resp.data
    assert 200 == resp.status_code


def test_api_app_info(client):
    resp = client.get("/api/app/info")
    assert b'{"build_time":null,"sha":null,"tags":null,"vc_version":"dev"}' in resp.data
    assert 200 == resp.status_code


def test_api_cluster_info(client):
    resp = client.get("/api/cluster/info")
    assert (
        b'[{"error":"Cluster http://foo:1234 not reachable!","id":0,"url":"http://foo:1234"}]'
        in resp.data
    )
    assert 200 == resp.status_code


@pytest.mark.parametrize("path", path_get_for_cluster)
def test_api_get_for_cluster(client, path):
    resp = client.get(path)
    assertNotReachable(resp)


@pytest.mark.parametrize("path", path_post_for_cluster)
def test_api_post_for_cluster(client, path):
    resp = client.post(path)
    assertNotReachable(resp)


@pytest.mark.parametrize("path", path_get_for_all)
def test_api_get_all(client, path):
    resp = client.get(path)
    assert b'"Cluster http://foo:1234 not reachable!"' in resp.data
    assert 200 == resp.status_code


def assertNotReachable(response):
    assert b'{"message":"Cluster http://foo:1234 not reachable!"}' in response.data
    assert 503 == response.status_code
