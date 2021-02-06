from app import util

def test_get_url(monkeypatch):
    assert util.get_url() == 'http://localhost:8083'

    monkeypatch.setenv('CONNECT_URL', 'http://connect:8083')
    assert util.get_url() == 'http://connect:8083'

def test_get_poll_intervall(monkeypatch):
    assert util.get_poll_intervall() == 60

    monkeypatch.setenv('VC_POLLING_INTERVAL_SEC', '30')
    assert util.get_poll_intervall() == 30

    monkeypatch.setenv('VC_POLLING_INTERVAL_SEC', 'FOO')
    assert util.get_poll_intervall() == 60

def test_get_request_timeout(monkeypatch):
    assert util.get_request_timeout() == 5

    monkeypatch.setenv('VC_REQUEST_TIMEOUT_SEC', '1')
    assert util.get_request_timeout() == 1

    monkeypatch.setenv('VC_REQUEST_TIMEOUT_SEC', 'FOO')
    assert util.get_request_timeout() == 5

def test_get_str_config(monkeypatch):
    assert util.get_str_config('FOO', 'BAR') == 'BAR'

    monkeypatch.setenv('FOO', 'BAZ')
    assert util.get_str_config('FOO', 'BAR') == 'BAZ'

def test_get_int_config(monkeypatch):
    assert util.get_int_config('FOO', 1) == 1

    monkeypatch.setenv('FOO', '100')
    assert util.get_int_config('FOO', '1') == 100