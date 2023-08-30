#!/bin/sh
export PGPASSWORD="test"
source /Users/antonstrokov/VSCode/ia_ras_anthropology/.env

filename="$(date +'%d-%m-%Y-%H-%M').dump"

# mkdir ~/pg_dumps

pg_dump -h $POSTGRES_HOST -p $POSTGRES_PORT -Fc -U $POSTGRES_USER $POSTGRES_DB > ~/pg_dumps/$filename

echo "Finished"