#!/bin/sh
set -e

echo "TZ: $TZ"
echo "LANG: $LANG"
echo "VC_SQLITE_FILE_PATH: $VC_SQLITE_FILE_PATH"

# SQL script to create db
SQL_SCRIPT="/dist/python/schema.sql"

# create db
if [ -f "$VC_SQLITE_FILE_PATH" ]; then
    echo "$VC_SQLITE_FILE_PATH exists already! The SQL script $SQL_SCRIPT is not executed."
else 
    echo "$VC_SQLITE_FILE_PATH does not exist. Running SQL script $SQL_SCRIPT."
    sqlite3 $VC_SQLITE_FILE_PATH < /dist/python/schema.sql 
    chown gunicorn:gunicorn $VC_SQLITE_FILE_PATH
fi

echo "Starting vue-connect"
echo "VC_VERSION: $VC_VERSION"
echo "VC_TAGS: $VC_TAGS"
echo "VC_CREATE_DB_IN_APP: $VC_CREATE_DB_IN_APP"
echo "VC_POLLING_INTERVAL_SEC: $VC_POLLING_INTERVAL_SEC"
echo "VC_REQUEST_TIMEOUT_SEC: $VC_REQUEST_TIMEOUT_SEC"
echo "CONNECT_URL: $CONNECT_URL"
    
exec /usr/bin/supervisord -c /etc/supervisord.conf
