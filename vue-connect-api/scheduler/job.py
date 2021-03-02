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
    def __init__(self):
        super().__init__(config.get_poll_intervall())

    def run(self):
        cache = store.CacheManager(config.get_db_url())
        try:
            logging.info("loading cluster state")
            state = connect.load_state()
            logging.info("merging cache")
            cache.merge(
                store.CacheEntry(
                    state=state,
                    running=True,
                    error_mesage=None,
                    last_time_running=datetime.now(),
                )
            )
        except ConnectionError:
            logging.info(
                config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(config.get_connect_url())
            )
            cache.merge(
                store.CacheEntry(
                    running=False,
                    error_mesage=config.ERROR_MSG_CLUSTER_NOT_REACHABLE.format(
                        config.get_connect_url()
                    ),
                )
            )

        except Timeout:

            logging.info(
                config.ERROR_MSG_CLUSTER_TIMEOUT.format(config.get_connect_url())
            )

            cache.merge(
                store.CacheEntry(
                    running=False,
                    error_mesage=config.ERROR_MSG_CLUSTER_TIMEOUT.format(
                        config.get_connect_url()
                    ),
                )
            )

        except Exception as e:

            logging.error("Could not update cache: %s", e)

            cache.merge(
                store.CacheEntry(
                    running=False, error_mesage=config.ERROR_MSG_INTERNAL_SERVER_ERROR
                )
            )
