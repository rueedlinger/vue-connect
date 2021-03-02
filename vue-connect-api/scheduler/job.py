import logging
from datetime import datetime

from common import config, connect, store
from requests.exceptions import ConnectionError, Timeout


class Job:
    def __init__(self, poll_intervall_sec):
        self._poll_intervall_sec = poll_intervall_sec

    def get_poll_intervall(self):
        return self._poll_intervall_sec

    def run(self):
        pass


class UpdateCacheJob(Job):
    def __init__(self, cluster_id):
        super().__init__(config.get_poll_intervall())
        self.cluster_id = cluster_id

    def run(self):
        cache = store.CacheManager(config.get_db_url())
        try:
            logging.info(
                "loading cluster state for clsuter id {}".format(self.cluster_id)
            )
            state = connect.load_state(self.cluster_id)
            logging.info("merging cache for cluster id {}".format(self.cluster_id))
            cache.merge(
                store.CacheEntry(
                    id=self.cluster_id,
                    state=state,
                    running=True,
                    error_mesage=None,
                    last_time_running=datetime.now(),
                )
            )
        except ConnectionError:
            logging.info(
                config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(
                    config.get_connect_url(self.cluster_id)
                )
            )
            cache.merge(
                store.CacheEntry(
                    id=self.cluster_id,
                    running=False,
                    error_mesage=config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(
                        config.get_connect_url(self.cluster_id)
                    ),
                )
            )

        except Timeout:

            logging.info(
                config.ERROR_MSG_CLUSTER_TIMEOUT.format(
                    config.get_connect_url(self.cluster_id)
                )
            )

            cache.merge(
                store.CacheEntry(
                    id=self.cluster_id,
                    running=False,
                    error_mesage=config.ERROR_MSG_CLUSTER_TIMEOUT.format(
                        config.get_connect_url(self.cluster_id)
                    ),
                )
            )

        except Exception as e:

            logging.error("Could not update cache: %s", e)

            cache.merge(
                store.CacheEntry(
                    id=self.cluster_id,
                    running=False,
                    error_mesage=config.ERROR_MSG_INTERNAL_SERVER_ERROR,
                )
            )
