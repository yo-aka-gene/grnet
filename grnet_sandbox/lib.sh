#!/bin/sh

USERNAME=$(whoami)

if [ $USERNAME = "jovyan" ]; then
    pip install --no-deps -r $(dirname $0)/config/requirements.txt
    pip install --no-deps -r $(dirname $0)/config/sandbox_reqs.txt
else
    VMNAME=$(basename $(dirname $(find . -name Dockerfile)) | tr '[A-Z]' '[a-z]')-jupyterlab-1
    docker exec --user jovyan $VMNAME pip install --no-deps -r /home/jovyan/config/requirements.txt
    docker exec --user jovyan $VMNAME pip install --no-deps -r /home/jovyan/config/sandbox_reqs.txt
fi
