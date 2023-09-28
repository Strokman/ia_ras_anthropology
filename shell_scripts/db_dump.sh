#!/bin/bash
echo &HOME
ENV_FILE="${HOME}/ia_ras_anthropology/.env"

source $ENV_FILE

FILENAME="$(date +'%Y-%m-%d-%H-%M').dump"
DIR="${HOME}/basehabilis_dumps"
CONTAINER="19f05141d779"

sudo docker exec $CONTAINER pg_dump -Fc -U $POSTGRES_USER $POSTGRES_DB > $DIR/$FILENAME