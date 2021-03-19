#!/bin/sh
set -e

echo "TZ: $TZ"
echo "LANG: $LANG"

echo "Starting vue-connect"
echo "VC_VERSION: $VC_VERSION"
echo "VC_TAGS: $VC_TAGS"
echo "VC_CREATE_DB_IN_APP: $VC_CREATE_DB_IN_APP"
echo "VC_POLLING_INTERVAL_SEC: $VC_POLLING_INTERVAL_SEC"
echo "VC_REQUEST_TIMEOUT_SEC: $VC_REQUEST_TIMEOUT_SEC"
echo "CONNECT_URL: $CONNECT_URL"
    
exec /usr/bin/supervisord -c /etc/supervisord.conf
