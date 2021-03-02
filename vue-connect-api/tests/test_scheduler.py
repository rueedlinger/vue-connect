from unittest.mock import patch

from scheduler import Scheduler, job

from tests import MockResp

TIMEOUT = 5


def test_add_job():

    scheduler = Scheduler()
    assert len(scheduler._scheduler._pending_jobs) == 0

    scheduler.add_job(job.Job(poll_intervall_sec=10))
    assert len(scheduler._scheduler._pending_jobs) == 1


def test_cache_job():

    cache = job.UpdateCacheJob(cluster_id=0)

    assert cache.get_poll_intervall() > 0

    patcher = patch("requests.get")
    mock_get = patcher.start()
    mock_get.return_value = MockResp(data=[])

    patcher_cache = patch("common.store.CacheManager")
    mock_cache = patcher_cache.start()

    cache.run()

    patcher.stop()
    patcher_cache.stop()

    mock_get.assert_called_once_with(
        "http://localhost:8083/connectors?expand=info&expand=status", timeout=TIMEOUT
    )

    mock_cache.assert_called_once_with("vue-connect.db")
