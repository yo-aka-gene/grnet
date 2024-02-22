#!/bin/sh
cd $(dirname $0)

get_id=$(id)
nb_id=${get_id[@]:4:3}
docker_name=$((basename $PWD) | tr '[A-Z]' '[a-z]')-jupyterlab-1

sed -i '' -e s/${docker_name}/CONTAINER_NAME/ docker-compose.yml
sed -i '' -e s/${nb_id}/YOUR_ID/ docker-compose.yml
git update-index --no-assume-unchanged docker-compose.yml
