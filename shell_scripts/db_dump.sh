#!/bin/bash

ENV_FILE="~/ia_ras_anthropology/.env"

source $ENV_FILE

FILENAME="$(date +'%Y-%m-%d-%H-%M').dump"
DIR="~/basehabilis_dumps"
CONTAINER="19f05141d779"

sudo docker exec $CONTAINER pg_dump -Fc -U $POSTGRES_USER $POSTGRES_DB > $DIR/$FILENAME