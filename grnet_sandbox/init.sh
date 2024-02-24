#!/bin/sh

VMNAME=$((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1

docker-compose up -d
sh auth.sh docker-compose.yml
docker compose up -d
docker start $VMNAME
docker exec --user jovyan $VMNAME sh /home/jovyan/lib.sh
docker exec --user jovyan $VMNAME sh /home/jovyan/writelib.sh
docker exec --user jovyan $VMNAME Rscript /home/jovyan/tools/set_renv.R
open http://localhost:8000
