from common.store import CacheEntry, CacheManager
from datetime import datetime


def get_cache_manager():
    cache = CacheManager(url=":memory:")
    with open("schema.sql", mode="r") as f:
        cache._db.cursor().executescript(f.read())

    return cache


def test_default_cache_entry():
    entry = CacheEntry()
    assert entry.id == 0
    assert entry.url is not None
    assert entry.running is None
    assert entry.state is None
    assert entry.last_time_running is None
    assert entry.error_mesage is None
    assert entry.created is not None

    assert entry.to_response() is not None
    assert entry.to_sql() is not None

    assert "state" in entry.to_response()
    assert [] == entry.to_response()["state"]

    assert len(entry.to_sql()) == 7

    assert "CLUSTER_ID" in entry.to_sql()
    assert entry.to_sql()["CLUSTER_ID"] == 0

    assert "CLUSTTER_URL" in entry.to_sql()
    assert entry.to_sql()["CLUSTTER_URL"] is not None

    assert "CLUSTER_STATE" in entry.to_sql()
    assert entry.to_sql()["CLUSTER_STATE"] is None

    assert "RUNNING" in entry.to_sql()
    assert entry.to_sql()["RUNNING"] is None

    assert "LAST_RUNNING_TIMESTAMP" in entry.to_sql()
    assert entry.to_sql()["LAST_RUNNING_TIMESTAMP"] is None

    assert "ERROR_MESSAGE" in entry.to_sql()
    assert entry.to_sql()["ERROR_MESSAGE"] is None

    assert "CREATED_TIMESTAMP" in entry.to_sql()
    assert entry.to_sql()["CREATED_TIMESTAMP"] is not None


def test_load():
    cache = get_cache_manager()
    resp = cache.load()
    assert resp is not None
    assert resp.state == []


def test_merge():
    cache = get_cache_manager()
    resp = cache.load()
    assert resp is not None
    assert resp.state == []
    assert resp.error_mesage is None
    assert resp.created is not None
    assert resp.running is None
    assert resp.last_time_running is None
    assert resp.id is not None
    assert resp.url is not None

    now = datetime.now()

    merged = cache.merge(CacheEntry(state={"foo": "bar"}, last_time_running=now))
    assert merged.state == {"foo": "bar"}
    assert merged.error_mesage is None
    assert merged.created is not None
    assert merged.running is None
    assert merged.last_time_running == now
    assert merged.id is not None
    assert merged.url is not None

    resp = cache.load()
    assert resp.state == {"foo": "bar"}
    assert resp.error_mesage is None
    assert resp.created is not None
    assert resp.last_time_running == now

    merged = cache.merge(CacheEntry(error_mesage="foo", running=True))
    assert merged.state == {"foo": "bar"}
    assert merged.error_mesage == "foo"
    assert merged.running == True

    resp = cache.load()
    assert resp.state == {"foo": "bar"}
    assert resp.error_mesage == "foo"
    assert resp.running == True


def test_merge_without_initial_load():
    cache = get_cache_manager()
    cache.merge(CacheEntry(state={"foo": "bar"}))
    cache.merge(CacheEntry(error_mesage="baz"))
    cache_entry = cache.load()

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

    cache.merge(CacheEntry(state=old_state))
    cache_entry = cache.merge(CacheEntry(state=new_state))

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

    cache.merge(CacheEntry(state=old_state))
    cache_entry = cache.merge(CacheEntry(state=new_state))

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

    cache.merge(CacheEntry(state=old_state))
    cache_entry = cache.merge(CacheEntry(state=new_state))

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

    cache.merge(CacheEntry(state=old_state))
    cache_entry = cache.merge(CacheEntry(state=new_state))

    assert "downtime" not in cache_entry.state[0]["connector"]
    assert "downtime" not in cache_entry.state[0]["tasks"][0]
