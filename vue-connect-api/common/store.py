import json
import logging
import sqlite3
from datetime import datetime

from common import config


class Cache:
    def __init__(self, url):
        self._url = url
        self._db = sqlite3.connect(url)

    def connect(self):
        self._db = sqlite3.connect(self._url)

    def close(self):
        self._db.close()

    def load_cache(self):
        select_sql = """SELECT CLUSTER_ID, CLUSTTER_URL, RUNNING, CLUSTER_STATE, ERROR_MESSAGE, CREATED_TIMESTAMP from VC_CLUSTER_CACHE where CLUSTER_ID=?"""

        db = self._db
        cur = db.cursor().execute(
            select_sql,
            (0,),
        )

        res = cur.fetchone()

        if res == None:
            return {"state": None}
        else:
            cache = dict(
                (cur.description[idx][0], value) for idx, value in enumerate(res)
            )

        return cache

    def new_cache(
        self, state=None, last_time_running=None, running=None, error_mesage=None
    ):
        cache = {}
        if state is not None:
            cache["CLUSTER_STATE"] = json.dumps(state)

        if last_time_running is not None:
            cache["LAST_RUNNING_TIMESTAMP"] = last_time_running

        if error_mesage is not None:
            cache["ERROR_MESSAGE"] = error_mesage

        if running is not None:
            cache["RUNNING"] = int(running)

        return cache

    def merge_cache(self, cache):
        update_sql = """INSERT OR REPLACE INTO VC_CLUSTER_CACHE (CLUSTER_ID, CLUSTTER_URL, RUNNING, CLUSTER_STATE, ERROR_MESSAGE, LAST_RUNNING_TIMESTAMP, CREATED_TIMESTAMP) values (?, ?, ?, ?, ?, ?, ?)"""
        select_sql = """SELECT CLUSTER_ID, CLUSTTER_URL, RUNNING, CLUSTER_STATE, ERROR_MESSAGE, LAST_RUNNING_TIMESTAMP, CREATED_TIMESTAMP from VC_CLUSTER_CACHE where CLUSTER_ID=?"""

        db = self._db
        cur = db.cursor().execute(
            select_sql,
            (0,),
        )

        res = cur.fetchone()
        old_cache = {}
        if res is not None:
            old_cache = dict(
                (cur.description[idx][0], value) for idx, value in enumerate(res)
            )

        self.__merge_value(cache, old_cache, "CLUSTER_STATE", "[]")
        self.__merge_value(cache, old_cache, "RUNNING", 1)
        self.__merge_value(cache, old_cache, "ERROR_MESSAGE", None)
        self.__merge_value(cache, old_cache, "LAST_RUNNING_TIMESTAMP", datetime.now())

        cur = db.cursor().execute(
            update_sql,
            (
                0,
                config.get_connect_url(),
                cache["RUNNING"],
                cache["CLUSTER_STATE"],
                cache["ERROR_MESSAGE"],
                cache["LAST_RUNNING_TIMESTAMP"],
                datetime.now(),
            ),
        )
        db.commit()

        return cache

    def __merge_value(self, new_cache, old_cache, key, defaul_value):
        if key not in new_cache:
            if key in old_cache:
                new_cache[key] = old_cache[key]
            else:
                new_cache[key] = defaul_value


def to_response(cache):

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
