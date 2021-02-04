#!/bin/sh
set -e

if [ -z "$@" ]; then
    echo "Starting vue-connect services"
    echo "VC_VERSION: $VC_VERSION"
    echo "VC_TAGS: $VC_TAGS"
    echo "VC_LABELS: $VC_LABELS"
    echo "VC_DIGEST: $VC_DIGEST"
    exec /usr/bin/supervisord -c /etc/supervisord.conf
else
    exec $@
fi