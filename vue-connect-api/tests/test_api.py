import pytest
import json

from app import app

path_get = [
    '/api/plugins',
    '/api/status/foo',
    '/api/config/foo',
    '/api/info'
]

path_post = [
    '/api/connectors/foo/tasks/0/restart',
    '/api/connectors/foo/resume',
    '/api/connectors/foo/pause',
    '/api/connectors/foo/delete',
    '/api/connectors/foo/restart'
]


@pytest.fixture
def client():

    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_api_not_found(client):
    resp = client.get('/foo')
    assert b'{"message":"Resource not found."}' in resp.data
    assert 404 == resp.status_code


def test_api_not_allowed(client):
    resp = client.post('/api/status', data=json.dumps({}),
                       content_type='application/json')
    assert b'{"message":"The method is not allowed for this resource."}' in resp.data
    assert 405 == resp.status_code


def test_api_missing_data_with_post(client):
    resp = client.post('/api/connectors/foo/config')
    assert b'{"message":"Missing data. There is no connector configuration for \'foo\'."}' in resp.data
    assert 400 == resp.status_code

    resp = client.post('/api/connectors')
    assert b'{"message":"Missing data. There was no connector configuration provided."}' in resp.data
    assert 400 == resp.status_code


def test_api_post_with_data(client):
    resp = client.post('/api/connectors/foo/config',
                       data=json.dumps({}),  content_type='application/json')
    assertNotReachable(resp)

    resp = client.post(
        '/api/connectors', data=json.dumps({'name': 'foo'}),  content_type='application/json')
    assertNotReachable(resp)

    resp = client.post('/api/connectors', data=json.dumps({}),
                       content_type='application/json')
    assert b'{"message":"Missing configuration property \'name\'."}' in resp.data
    assert 400 == resp.status_code


def test_api_polling(client):
    resp = client.get('/api/polling')
    assert b'{"isConnectUp":false,"loadtime":0,"message":"Cluster http://localhost:8083 not reachable!","state":null}' in resp.data
    assert 200 == resp.status_code


def test_api_app_info(client):
    resp = client.get('/api/app/info')
    assert b'{"build_time":null,"sha":null,"tags":null,"vc_version":"dev"}' in resp.data
    assert 200 == resp.status_code


@pytest.mark.parametrize("path", path_get)
def test_api_get(client, path):
    resp = client.get(path)
    assertNotReachable(resp)


@pytest.mark.parametrize("path", path_post)
def test_api_post(client, path):
    resp = client.post(path)
    assertNotReachable(resp)


def assertNotReachable(response):
    assert b'{"message":"Cluster http://localhost:8083 not reachable!"}' in response.data
    assert 503 == response.status_code
