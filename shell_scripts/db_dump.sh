#!/bin/sh
export PGPASSWORD="test"
source /Users/antonstrokov/VSCode/ia_ras_anthropology/.env

filename="$(date +'%Y-%m-%d-%H-%M').dump"

#on the prod - give full path mandatory
pg_dump -h $POSTGRES_HOST -p $POSTGRES_PORT -Fc -U $POSTGRES_USER $POSTGRES_DB > ~/pg_dumps/$filename
