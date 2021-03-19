from datetime import datetime

import fakeredis
from common import config
from common.store import CacheEntry, CacheManager


def get_cache_manager():
    cache = CacheManager(fakeredis.FakeStrictRedis())
    return cache


def test_from_dict():

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

    entry = CacheEntry.from_dict({})
    assert entry.state == []

    entry = CacheEntry.from_dict({"CLUSTER_STATE": None})
    assert entry.state == []

    entry = CacheEntry.from_dict({"CLUSTER_STATE": {"foo": "bar"}})
    assert entry.state == {"foo": "bar"}

    entry = CacheEntry.from_dict({"CLUSTER_ID": 0})
    assert entry.id == 0

    entry = CacheEntry.from_dict({"CLUSTER_ID": None})
    assert entry.id is None

    entry = CacheEntry.from_dict({"CLUSTER_URL": "foo"})
    assert entry.url == "foo"

    entry = CacheEntry.from_dict({"CLUSTER_URL": None})
    assert entry.url is None

    entry = CacheEntry.from_dict({"RUNNING": True})
    assert entry.running == True

    entry = CacheEntry.from_dict({"RUNNING": False})
    assert entry.running == False

    entry = CacheEntry.from_dict({"RUNNING": None})
    assert entry.running is None

    entry = CacheEntry.from_dict({"ERROR_MESSAGE": None})
    assert entry.error_mesage is None

    entry = CacheEntry.from_dict({"ERROR_MESSAGE": ""})
    assert entry.error_mesage is None

    entry = CacheEntry.from_dict({"ERROR_MESSAGE": "foo"})
    assert entry.error_mesage == "foo"

    entry = CacheEntry.from_dict({"LAST_RUNNING_TIMESTAMP": None})
    assert entry.last_time_running is None

    entry = CacheEntry.from_dict(
        {"LAST_RUNNING_TIMESTAMP": "2021-03-01 23:05:53.419967"}
    )
    assert entry.last_time_running is not None
    assert entry.last_time_running == datetime.strptime(
        "2021-03-01 23:05:53.419967", DATE_FORMAT
    )

    entry = CacheEntry.from_dict({"CREATED_TIMESTAMP": "2021-03-01 23:05:53.419967"})
    assert entry.created is not None
    assert entry.created == datetime.strptime("2021-03-01 23:05:53.419967", DATE_FORMAT)


def test_default_cache_entry():
    entry = CacheEntry()
    assert entry.id is None
    assert entry.url is None
    assert entry.running is None
    assert entry.state is None
    assert entry.last_time_running is None
    assert entry.error_mesage is None
    assert entry.created is not None

    assert entry.get_state() == []
    assert entry.to_dict() is not None

    assert len(entry.to_dict()) == 7

    assert "CLUSTER_ID" in entry.to_dict()
    assert entry.to_dict()["CLUSTER_ID"] is None

    assert "CLUSTER_URL" in entry.to_dict()
    assert entry.to_dict()["CLUSTER_URL"] is None

    assert "CLUSTER_STATE" in entry.to_dict()
    assert entry.to_dict()["CLUSTER_STATE"] is None

    assert "RUNNING" in entry.to_dict()
    assert entry.to_dict()["RUNNING"] is None

    assert "LAST_RUNNING_TIMESTAMP" in entry.to_dict()
    assert entry.to_dict()["LAST_RUNNING_TIMESTAMP"] is None

    assert "ERROR_MESSAGE" in entry.to_dict()
    assert entry.to_dict()["ERROR_MESSAGE"] is None

    assert "CREATED_TIMESTAMP" in entry.to_dict()
    assert entry.to_dict()["CREATED_TIMESTAMP"] is not None


def test_load():
    cache = get_cache_manager()
    resp = cache.load(0)
    assert resp is not None
    assert resp.state == []
    assert resp.id == 0
    assert resp.url == config.get_connect_url(0)


def test_merge():
    cache = get_cache_manager()
    resp = cache.load(0)
    assert resp is not None
    assert resp.state == []
    assert resp.error_mesage is None
    assert resp.created is not None
    assert resp.running is None
    assert resp.last_time_running is None
    assert resp.id == 0
    assert resp.url == config.get_connect_url(0)

    now = datetime.now()

    merged = cache.merge(CacheEntry(id=0, state={"foo": "bar"}, last_time_running=now))
    assert merged.state == {"foo": "bar"}
    assert merged.error_mesage is None
    assert merged.created is not None
    assert merged.running is None
    assert merged.last_time_running == now
    assert merged.id == 0
    assert merged.url == config.get_connect_url(0)

    resp = cache.load(0)
    assert resp.state == {"foo": "bar"}
    assert resp.error_mesage is None
    assert resp.created is not None
    assert resp.last_time_running == now
    assert resp.id == 0
    assert resp.url == config.get_connect_url(0)

    merged = cache.merge(CacheEntry(id=0, error_mesage="foo", running=True))
    assert merged.state == {"foo": "bar"}
    assert merged.error_mesage == "foo"
    assert merged.running == True

    resp = cache.load(0)
    assert resp.state == {"foo": "bar"}
    assert resp.error_mesage == "foo"
    assert resp.running == True
    assert resp.id == 0
    assert resp.url == config.get_connect_url(0)


def test_merge_without_initial_load():
    cache = get_cache_manager()
    cache.merge(CacheEntry(id=0, state={"foo": "bar"}))
    cache.merge(CacheEntry(id=0, error_mesage="baz"))
    cache_entry = cache.load(0)

    assert cache_entry.state == {"foo": "bar"}
    assert cache_entry.error_mesage == "baz"


def test_downtime_both():

    cache = get_cache_manager()

    old_state = [
        {
            "name": "foo",
            "connector": {"state": "FAILED", "downtime": "2021-02-01T10:10:10.000000"},
            "tasks": [
                {"state": "FAILED", "downtime": "2021-02-01T10:10:10.000000"},
            ],
        },
    ]

    new_state = [
        {
            "name": "foo",
            "connector": {"state": "FAILED", "downtime": "2021-03-01T21:24:25.883837"},
            "tasks": [
                {"state": "FAILED", "downtime": "2021-03-01T21:24:25.883837"},
            ],
        }
    ]

    cache.merge(CacheEntry(id=0, state=old_state))
    cache_entry = cache.merge(CacheEntry(id=0, state=new_state))

    assert cache_entry.state[0]["connector"]["downtime"] == "2021-02-01T10:10:10.000000"
    assert cache_entry.state[0]["tasks"][0]["downtime"] == "2021-02-01T10:10:10.000000"


def test_downtime_connector():

    cache = get_cache_manager()

    old_state = [
        {
            "name": "foo",
            "connector": {"state": "FAILED", "downtime": "2021-02-01T10:10:10.000000"},
            "tasks": [
                {"state": "RUNNING"},
            ],
        },
    ]

    new_state = [
        {
            "name": "foo",
            "connector": {"state": "FAILED", "downtime": "2021-03-01T21:24:25.883837"},
            "tasks": [
                {"state": "RUNNING"},
            ],
        }
    ]

    cache.merge(CacheEntry(id=0, state=old_state))
    cache_entry = cache.merge(CacheEntry(id=0, state=new_state))

    assert cache_entry.state[0]["connector"]["downtime"] == "2021-02-01T10:10:10.000000"
    assert "downtime" not in cache_entry.state[0]["tasks"][0]


def test_downtime_connector_only_task():

    cache = get_cache_manager()

    old_state = [
        {
            "name": "foo",
            "connector": {"state": "RUNNING"},
            "tasks": [
                {"state": "FAILED", "downtime": "2021-02-01T10:10:10.000000"},
            ],
        },
    ]

    new_state = [
        {
            "name": "foo",
            "connector": {"state": "RUNNING"},
            "tasks": [
                {"state": "FAILED", "downtime": "2021-03-01T21:24:25.883837"},
            ],
        }
    ]

    cache.merge(CacheEntry(id=0, state=old_state))
    cache_entry = cache.merge(CacheEntry(id=0, state=new_state))

    assert cache_entry.state[0]["tasks"][0]["downtime"] == "2021-02-01T10:10:10.000000"
    assert "downtime" not in cache_entry.state[0]["connector"]


def test_no_merge_downtime():

    cache = get_cache_manager()

    old_state = [
        {
            "name": "foo",
            "connector": {"state": "FAILED", "downtime": "2021-02-01T10:10:10.000000"},
            "tasks": [
                {"state": "FAILED", "downtime": "2021-02-01T10:10:10.000000"},
            ],
        },
    ]

    new_state = [
        {
            "name": "foo",
            "connector": {"state": "RUNNING"},
            "tasks": [
                {"state": "RUNNING"},
            ],
        }
    ]

    cache.merge(CacheEntry(id=0, state=old_state))
    cache_entry = cache.merge(CacheEntry(id=0, state=new_state))

    assert "downtime" not in cache_entry.state[0]["connector"]
    assert "downtime" not in cache_entry.state[0]["tasks"][0]
