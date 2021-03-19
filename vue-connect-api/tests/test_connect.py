from unittest.mock import patch

import pytest
from common import connect

from tests import MockResp

TIMEOUT = 5

status_repsonses = [None, {}, {"foo": {}}, {"foo": {"status": {}}}]


@pytest.mark.parametrize("data", status_repsonses)
def test_load_state(data):
    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(data=data)

    resp = connect.load_state(0)
    patcherGet.stop()

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert resp == []


def test_cluster_info():
    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(
        data={"foo": {"status": {"connector": {}, "tasks": []}}}
    )

    resp = connect.load_state(0)
    patcherGet.stop()

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert resp[0]["cluster"] is not None
    assert resp[0]["cluster"]["url"] is not None
    assert resp[0]["cluster"]["id"] is not None


def test_error_message():
    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(
        data={"foo": {"status": {"connector": {"trace": "foo"}}}}
    )

    resp = connect.load_state(0)
    patcherGet.stop()

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert resp[0]["connector"]["traceShort"] == "foo"
    assert resp[0]["connector"]["trace"] == "foo"
    assert resp[0]["connector"]["downtime"] is not None


def test_error_message_task():
    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(
        data={"foo": {"status": {"tasks": [{"trace": "foo"}]}}}
    )

    resp = connect.load_state(0)
    patcherGet.stop()

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert resp[0]["tasks"][0]["traceShort"] == "foo"
    assert resp[0]["tasks"][0]["trace"] == "foo"
    assert resp[0]["tasks"][0]["downtime"] is not None


def test_trace_short():
    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(
        data={"foo": {"status": {"connector": {"trace": "foo\nbar"}}}}
    )

    resp = connect.load_state(0)
    patcherGet.stop()

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert resp[0]["connector"]["traceShort"] == "foo"
    assert resp[0]["connector"]["trace"] == "foo\nbar"
    assert resp[0]["connector"]["downtime"] is not None


def test_trace_short_task():
    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(
        data={"foo": {"status": {"tasks": [{"trace": "foo\nbar"}]}}}
    )

    resp = connect.load_state(0)
    patcherGet.stop()

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert resp[0]["tasks"][0]["traceShort"] == "foo"
    assert resp[0]["tasks"][0]["trace"] == "foo\nbar"
    assert resp[0]["tasks"][0]["downtime"] is not None


def test_stacktrace_full():

    stacktrace = """java.lang.Exception: Stack trace
at java.base/java.lang.Thread.dumpStack(Thread.java:1383)
at com.ericgoebelbecker.stacktraces.StackTrace.d(StackTrace.java:23)
"""

    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(
        data={"foo": {"status": {"connector": {"trace": stacktrace}}}}
    )

    resp = connect.load_state(0)
    patcherGet.stop()

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert resp[0]["connector"]["traceShort"] == "java.lang.Exception: Stack trace"
    assert resp[0]["connector"]["traceException"] == "java.lang.Exception"
    assert resp[0]["connector"]["trace"] == stacktrace
    assert resp[0]["connector"]["downtime"] is not None


def test_stacktrace_full_task():

    stacktrace = """java.lang.Exception: Stack trace
at java.base/java.lang.Thread.dumpStack(Thread.java:1383)
at com.ericgoebelbecker.stacktraces.StackTrace.d(StackTrace.java:23)
"""

    patcherGet = patch("requests.get")
    mock_get = patcherGet.start()
    mock_get.return_value = MockResp(
        data={"foo": {"status": {"tasks": [{"trace": stacktrace}]}}}
    )

    resp = connect.load_state(0)
    patcherGet.stop()

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    assert resp[0]["tasks"][0]["traceShort"] == "java.lang.Exception: Stack trace"
    assert resp[0]["tasks"][0]["traceException"] == "java.lang.Exception"
    assert resp[0]["tasks"][0]["trace"] == stacktrace
    assert resp[0]["tasks"][0]["downtime"] is not None
