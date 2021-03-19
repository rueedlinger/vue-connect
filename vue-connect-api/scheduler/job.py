from datetime import datetime

from common import config, connect, store
from requests.exceptions import ConnectionError, Timeout

logger = config.get_logger("job")


class Job:
    def __init__(self, poll_intervall_sec):
        self._poll_intervall_sec = poll_intervall_sec

    def get_poll_intervall(self):
        return self._poll_intervall_sec

    def run(self):
        pass


class UpdateCacheJob(Job):
    def __init__(self):
        super().__init__(config.get_poll_intervall())

    def run(self):
        cache = store.CacheManager(config.get_redis())
        for cluster in config.get_connect_clusters():
            try:
                cluster_id = cluster["id"]
                logger.info("loading cluster state {}".format(cluster))
                state = connect.load_state(cluster_id)
                logger.info("merging cache {}".format(cluster))
                cache.merge(
                    store.CacheEntry(
                        id=cluster_id,
                        state=state,
                        running=True,
                        error_mesage=None,
                        last_time_running=datetime.now(),
                    )
                )
                logger.info("cache updated {}".format(cluster))
            except ConnectionError:
                logger.info(
                    config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(
                        config.get_connect_url(cluster_id)
                    )
                )
                cache.merge(
                    store.CacheEntry(
                        id=cluster_id,
                        running=False,
                        error_mesage=config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(
                            config.get_connect_url(cluster_id)
                        ),
                    )
                )

            except Timeout:

                logger.info(
                    config.ERROR_MSG_CLUSTER_TIMEOUT.format(
                        config.get_connect_url(cluster_id)
                    )
                )

                cache.merge(
                    store.CacheEntry(
                        id=cluster_id,
                        running=False,
                        error_mesage=config.ERROR_MSG_CLUSTER_TIMEOUT.format(
                            config.get_connect_url(cluster_id)
                        ),
                    )
                )

            except Exception as e:
                logger.error("Could not update cache: %s", e)
