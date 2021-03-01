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

        DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

        kwargs = {}
        if "CLUSTER_ID" in sqlRow:
            kwargs["id"] = sqlRow["CLUSTER_ID"]

        if "CLUSTER_URL" in sqlRow:
            kwargs["url"] = sqlRow["CLUSTER_URL"]

        if "CLUSTER_STATE" in sqlRow and sqlRow["CLUSTER_STATE"] is not None:
            kwargs["state"] = json.loads(sqlRow["CLUSTER_STATE"])
        else:
            kwargs["state"] = []

        if "RUNNING" in sqlRow:
            kwargs["running"] = bool(sqlRow["RUNNING"])

        if "ERROR_MESSAGE" in sqlRow:
            if (
                sqlRow["ERROR_MESSAGE"] is not None
                and len(sqlRow["ERROR_MESSAGE"]) == 0
            ):
                kwargs["error_mesage"] = None
            else:
                kwargs["error_mesage"] = sqlRow["ERROR_MESSAGE"]

        if (
            "LAST_RUNNING_TIMESTAMP" in sqlRow
            and sqlRow["LAST_RUNNING_TIMESTAMP"] is not None
        ):
            kwargs["last_time_running"] = datetime.strptime(
                sqlRow["LAST_RUNNING_TIMESTAMP"], DATE_FORMAT
            )

        if "CREATED_TIMESTAMP" in sqlRow and sqlRow["CREATED_TIMESTAMP"] is not None:
            kwargs["created"] = datetime.strptime(
                sqlRow["CREATED_TIMESTAMP"], DATE_FORMAT
            )

        return CacheEntry(**kwargs)

    def to_sql(self):

        return {
            "CLUSTER_ID": self.id,
            "CLUSTER_URL": self.url,
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
        select_sql = """SELECT * from VC_CLUSTER_CACHE where CLUSTER_ID=?"""

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
        update_sql = """INSERT OR REPLACE INTO VC_CLUSTER_CACHE (CLUSTER_ID, CLUSTER_URL, RUNNING, CLUSTER_STATE, ERROR_MESSAGE, LAST_RUNNING_TIMESTAMP, CREATED_TIMESTAMP) values (:CLUSTER_ID, :CLUSTER_URL, :RUNNING, :CLUSTER_STATE, :ERROR_MESSAGE, :LAST_RUNNING_TIMESTAMP, :CREATED_TIMESTAMP)"""
        select_sql = """SELECT * from VC_CLUSTER_CACHE where CLUSTER_ID=?"""

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

                self._merge_state(new_cache=cache_entry, old_cache=old_cache)
                self._merge_error(new_cache=cache_entry, old_cache=old_cache)

                self._merge_last_time_running(
                    new_cache=cache_entry, old_cache=old_cache
                )
                self._merge_running(new_cache=cache_entry, old_cache=old_cache)
                self._merge_url(new_cache=cache_entry, old_cache=old_cache)

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