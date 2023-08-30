#!/bin/sh
export PGPASSWORD="test"
source .env

filename="$(date +'%d-%m-%Y').dump"
dir='~/pg_dumps'
mkdir dir
pg_dump -h $POSTGRES_HOST -p $POSTGRES_PORT -Fc -U $POSTGRES_USER $POSTGRES_DB > $dir/$filename

pg_restore --clean -h 192.168.1.57 -p 52432 -d test -U test $dir/$filename

