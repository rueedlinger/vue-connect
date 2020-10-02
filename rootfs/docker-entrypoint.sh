#!/bin/sh
set -e

if [ -z "$@" ]; then
    echo "Starting vue-connect services"
    exec /usr/bin/supervisord -c /etc/supervisord.conf
else
    exec $@
fi