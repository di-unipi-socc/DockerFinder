#!/usr/bin/env bash


exec ./start_scanner.py "$@"

#
#set -e
#
#if [ "$1" = 'scanner' ]; then
#    chown -R postgres "$PGDATA"
#
#    if [ -z "$(ls -A "$PGDATA")" ]; then
#        gosu postgres initdb
#    fi
#
#    exec gosu postgres "$@"
#fi
#
#exec "$@"