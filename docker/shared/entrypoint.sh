#!/bin/bash

set -e

cmd="$@"

if [ $# = 0 ]; then
    cmd="sleep infinity"
fi

# auto enable sshd
/usr/sbin/sshd
exec /usr/local/bin/dumb-init -- $cmd
