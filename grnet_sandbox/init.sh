#!/bin/sh

VMNAME=$((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1

docker-compose up -d
sh auth.sh docker-compose.yml
docker compose up -d
docker start $VMNAME
open http://localhost:8000
