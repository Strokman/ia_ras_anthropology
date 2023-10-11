#!/bin/bash

ENV_FILE="${HOME}/ia_ras_anthropology/.env"

source $ENV_FILE

FILENAME="$(date +'%Y-%m-%d-%H-%M').dump"
DIR="${HOME}/basehabilis_dumps"
CONTAINER="ia_ras_anthropology-db-1"

sudo docker exec $CONTAINER pg_dump -Fc -U $POSTGRES_USER $POSTGRES_DB > $DIR/$FILENAME