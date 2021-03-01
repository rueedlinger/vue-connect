import json
import logging
import sqlite3
from datetime import datetime

from common import config


class CacheEntry:
    def __init__(
        self,
        id=0,
        url=config.get_connect_url(),
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
    def from_sql(sqlRow):

        kwargs = {}
        if "CLUSTER_ID" in sqlRow:
            kwargs["id"] = sqlRow["CLUSTER_ID"]

        if "CLUSTTER_URL" in sqlRow:
            kwargs["url"] = sqlRow["CLUSTTER_URL"]

        if "CLUSTER_STATE" in sqlRow:
            kwargs["state"] = json.loads(sqlRow["CLUSTER_STATE"])

        if "RUNNING" in sqlRow:
            kwargs["running"] = bool(sqlRow["RUNNING"])

        if "ERROR_MESSAGE" in sqlRow:
            kwargs["error_mesage"] = sqlRow["ERROR_MESSAGE"]

        if "LAST_RUNNING_TIMESTAMP" in sqlRow:
            kwargs["last_time_running"] = sqlRow["LAST_RUNNING_TIMESTAMP"]

        if "CREATED_TIMESTAMP" in sqlRow:
            kwargs["created"] = sqlRow["CREATED_TIMESTAMP"]

        return CacheEntry(**kwargs)

    def to_sql(self):

        return {
            "CLUSTER_ID": self.id,
            "CLUSTTER_URL": self.url,
            "CLUSTER_STATE": json.dumps(self.state) if self.state is not None else None,
            "RUNNING": int(self.running) if self.running is not None else None,
            "LAST_RUNNING_TIMESTAMP": self.last_time_running,
            "ERROR_MESSAGE": self.error_mesage,
            "CREATED_TIMESTAMP": self.created,
        }

    def to_response(self):

        out = {}

        if self.state is not None:
            out["state"] = self.state
        else:
            out["state"] = []

        if self.error_mesage is not None:
            out["message"] = self.error_mesage

        if self.running is not None:
            out["isConnectUp"] = self.running

        return out


class CacheManager:
    def __init__(self, url):
        self._url = url
        self._db = sqlite3.connect(url)

    def connect(self):
        self._db = sqlite3.connect(self._url)

    def close(self):
        self._db.close()

    def load(self):
        select_sql = """SELECT CLUSTER_ID, CLUSTTER_URL, RUNNING, CLUSTER_STATE, ERROR_MESSAGE, CREATED_TIMESTAMP from VC_CLUSTER_CACHE where CLUSTER_ID=?"""

        db = self._db
        cur = db.cursor().execute(
            select_sql,
            (0,),
        )

        res = cur.fetchone()

        if res == None:
            return CacheEntry(state=[])
        else:
            return CacheEntry.from_sql(
                dict((cur.description[idx][0], value) for idx, value in enumerate(res))
            )

    def merge(self, cache_entry: CacheEntry):
        update_sql = """INSERT OR REPLACE INTO VC_CLUSTER_CACHE (CLUSTER_ID, CLUSTTER_URL, RUNNING, CLUSTER_STATE, ERROR_MESSAGE, LAST_RUNNING_TIMESTAMP, CREATED_TIMESTAMP) values (:CLUSTER_ID, :CLUSTTER_URL, :RUNNING, :CLUSTER_STATE, :ERROR_MESSAGE, :LAST_RUNNING_TIMESTAMP, :CREATED_TIMESTAMP)"""
        select_sql = """SELECT CLUSTER_ID, CLUSTTER_URL, RUNNING, CLUSTER_STATE, ERROR_MESSAGE, LAST_RUNNING_TIMESTAMP, CREATED_TIMESTAMP from VC_CLUSTER_CACHE where CLUSTER_ID=?"""

        db = self._db

        with db:
            # explicit begin transaction before reading data
            db.execute("BEGIN")

            cursor = db.cursor()
            cursor.execute(
                select_sql,
                (cache_entry.id,),
            )

            res = cursor.fetchone()
            # is there already an entry in the cache
            if res is not None:
                old_cache = CacheEntry.from_sql(
                    dict(
                        (cursor.description[idx][0], value)
                        for idx, value in enumerate(res)
                    )
                )

                if (
                    cache_entry.error_mesage is None
                    and old_cache.error_mesage is not None
                ):
                    cache_entry.error_mesage = old_cache.error_mesage

                else:
                    if len(cache_entry.error_mesage) == 0:
                        cache_entry.error_mesage = None

                if (
                    cache_entry.last_time_running is None
                    and old_cache.last_time_running is not None
                ):
                    cache_entry.last_time_running = old_cache.last_time_running

                if cache_entry.running is None and old_cache.running is not None:
                    cache_entry.running = old_cache.running

                if cache_entry.created is None and old_cache.created is not None:
                    cache_entry.created = old_cache.created

                if cache_entry.state is None and old_cache.state is not None:
                    cache_entry.state = old_cache.state

                if cache_entry.url is None and old_cache.url is not None:
                    cache_entry.url = old_cache.url

                cursor.execute(
                    update_sql,
                    cache_entry.to_sql(),
                )

            else:
                cursor.execute(
                    update_sql,
                    cache_entry.to_sql(),
                )

        return cache_entry


def to_dict(cache: CacheEntry):

    resp = {}

    if "CLUSTER_STATE" in cache and cache["CLUSTER_STATE"] is not None:
        resp["state"] = json.loads(cache["CLUSTER_STATE"])
    else:
        resp["state"] = []

    if "ERROR_MESSAGE" in cache and cache["ERROR_MESSAGE"] is not None:
        resp["message"] = cache["ERROR_MESSAGE"]

    if "RUNNING" in cache and cache["RUNNING"] is not None:
        resp["isConnectUp"] = bool(cache["RUNNING"])

    return resp
