#!/bin/sh

USERNAME=$(whoami)

if [ $USERNAME = "jovyan" ]; then
    pip list --format=freeze > $(dirname $0)/config/sandbox_reqs.txt
else
    VMNAME=$(basename $(dirname $(find . -name Dockerfile)) | tr '[A-Z]' '[a-z]')-jupyterlab-1
    docker exec --user jovyan $VMNAME sh /home/jovyan/writelib.sh
fi
