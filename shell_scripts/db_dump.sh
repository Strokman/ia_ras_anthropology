#!/bin/bash
source ~/ia_ras_anthropology/.env

FILENAME="$(date +'%Y-%m-%d-%H-%M').dump"

sudo docker exec 19f05141d779 pg_dump -Fc -U $POSTGRES_USER $POSTGRES_DB > ~/basehabilis_dumps/$FILENAME