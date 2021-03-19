import json
from datetime import datetime

import redis

from common import config

logger = config.get_logger("store")


class CacheEntry:
    def __init__(
        self,
        id=None,
        url=None,
        state=None,
        last_time_running=None,
        running=None,
        error_mesage=None,
        created=datetime.now(),
    ):
        self.id = id
        self.url = url
        self.state = state
        self.last_time_running = last_time_running
        self.running = running
        self.error_mesage = error_mesage
        self.created = created

    @staticmethod
    def from_dict(data):

        kwargs = {}
        if "CLUSTER_ID" in data:
            kwargs["id"] = data["CLUSTER_ID"]

        if "CLUSTER_URL" in data:
            kwargs["url"] = data["CLUSTER_URL"]

        if "CLUSTER_STATE" in data and data["CLUSTER_STATE"] is not None:
            kwargs["state"] = data["CLUSTER_STATE"]
        else:
            kwargs["state"] = []

        if "RUNNING" in data:
            kwargs["running"] = data["RUNNING"]

        if (
            "ERROR_MESSAGE" in data
            and data["ERROR_MESSAGE"] is not None
            and len(data["ERROR_MESSAGE"]) > 0
        ):
            kwargs["error_mesage"] = data["ERROR_MESSAGE"]

        if (
            "LAST_RUNNING_TIMESTAMP" in data
            and data["LAST_RUNNING_TIMESTAMP"] is not None
        ):

            kwargs["last_time_running"] = datetime.fromisoformat(
                data["LAST_RUNNING_TIMESTAMP"]
            )

        if "CREATED_TIMESTAMP" in data and data["CREATED_TIMESTAMP"] is not None:
            kwargs["created"] = datetime.fromisoformat(data["CREATED_TIMESTAMP"])

        return CacheEntry(**kwargs)

    def get_state(self):
        if self.state is None:
            return []
        else:
            return self.state

    def to_dict(self):

        return {
            "CLUSTER_ID": self.id,
            "CLUSTER_URL": self.url,
            "CLUSTER_STATE": self.state,
            "RUNNING": self.running,
            "LAST_RUNNING_TIMESTAMP": self.last_time_running.isoformat()
            if self.last_time_running is not None
            else None,
            "ERROR_MESSAGE": self.error_mesage,
            "CREATED_TIMESTAMP": self.created.isoformat()
            if self.created is not None
            else None,
        }

    def __eq__(self, other: object) -> bool:
        return self.to_dict() == other.to_dict()

    def __str__(self) -> str:
        return str(self.to_dict())


class CacheManager:
    def __init__(self, redis_connection: redis.Redis):
        self._redis = redis_connection

    def close(self):
        pass

    def load(self, id):

        res = self._redis.get(id)

        if res == None:
            return CacheEntry(id=id, url=config.get_connect_url(id), state=[])
        else:
            return CacheEntry.from_dict(json.loads(res))

    def merge(self, cache_entry: CacheEntry):

        cache_ttl = config.get_cache_ttl()

        if cache_entry.id is None:
            raise AssertionError("cache entry id is not set!")

        if cache_entry.url is None:
            cache_entry.url = config.get_connect_url(cache_entry.id)

        redis = self._redis

        res = redis.get(cache_entry.id)

        # is there already an entry in the cache
        if res is not None:
            old_cache = CacheEntry.from_dict(json.loads(res))

            self._merge_state(new_cache=cache_entry, old_cache=old_cache)

            self._merge_last_time_running(new_cache=cache_entry, old_cache=old_cache)
            self._merge_created(new_cache=cache_entry, old_cache=old_cache)

            # only merge error message when state was not running
            if cache_entry.running == False:
                self._merge_error(new_cache=cache_entry, old_cache=old_cache)

            self._merge_running(new_cache=cache_entry, old_cache=old_cache)
            self._merge_url(new_cache=cache_entry, old_cache=old_cache)

            # only update cache when state was updated the last seconds
            if cache_entry != old_cache:
                redis.set(
                    cache_entry.id, json.dumps(cache_entry.to_dict()), ex=cache_ttl
                )
            else:
                logger.info(
                    "The cache entry for cluster state (id '{}') will not be updated, because there were no changes.".format(
                        cache_entry.id
                    )
                )

        else:

            redis.set(cache_entry.id, json.dumps(cache_entry.to_dict()), ex=cache_ttl)

        return cache_entry

    def _merge_state(self, new_cache, old_cache):
        if new_cache.state is None and old_cache.state is not None:
            new_cache.state = old_cache.state
        else:
            self._merge_donwtime(new_cache=new_cache, old_cache=old_cache)

    def _merge_url(self, new_cache, old_cache):
        if new_cache.url is None and old_cache.url is not None:
            new_cache.url = old_cache.url

    def _merge_running(self, new_cache, old_cache):
        if new_cache.running is None and old_cache.running is not None:
            new_cache.running = old_cache.running

    def _merge_created(self, new_cache, old_cache):
        if old_cache.created is not None:
            new_cache.created = old_cache.created

    def _merge_last_time_running(self, new_cache, old_cache):
        if (
            new_cache.last_time_running is None
            and old_cache.last_time_running is not None
        ):
            new_cache.last_time_running = old_cache.last_time_running

    def _merge_donwtime(self, new_cache, old_cache):
        failed = {}
        for connector in old_cache.state:
            name = connector["name"]
            if connector["connector"]["state"] == "FAILED":
                failed[name] = connector["connector"]["downtime"]

            for i, task in enumerate(connector["tasks"]):
                if task["state"] == "FAILED":
                    failed[name + ":" + str(i)] = task["downtime"]

        if len(failed) > 0:
            for connector in new_cache.state:
                name = connector["name"]
                if connector["connector"]["state"] == "FAILED":

                    if name in failed:
                        connector["connector"]["downtime"] = failed[name]

                for i, task in enumerate(connector["tasks"]):
                    if task["state"] == "FAILED":
                        task_id = name + ":" + str(i)
                        if task_id in failed:
                            connector["tasks"][i]["downtime"] = failed[task_id]

    def _merge_error(self, new_cache, old_cache):
        if new_cache.error_mesage is None and old_cache.error_mesage is not None:
            new_cache.error_mesage = old_cache.error_mesage
