#!/bin/sh
set -e

if [ -z "$@" ]; then
    echo "Starting vue-connect"
    echo "VC_VERSION: $VC_VERSION"
    echo "VC_TAGS: $VC_TAGS"
    echo "CONNECT_URL: $CONNECT_URL"
    exec /usr/bin/supervisord -c /etc/supervisord.conf
else
    exec $@
fi