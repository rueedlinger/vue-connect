import logging
import time
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
        cache = store.Cache(config.get_db_url())
        try:
            state = connect.load_state()
            cache.merge_cache(
                cache.new_cache(
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
            cache.merge_cache(
                cache.new_cache(
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

            cache.merge_cache(
                cache.new_cache(
                    running=False,
                    error_mesage=config.ERROR_MSG_CLUSTER_TIMEOUT.format(
                        config.get_connect_url()
                    ),
                )
            )

        except Exception as e:

            logging.error("Could not update cache: %s", e)

            cache.merge_cache(
                cache.new_cache(
                    running=False, error_mesage=config.ERROR_MSG_INTERNAL_SERVER_ERROR
                )
            )
