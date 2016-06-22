#!/bin/bash


sudo mkdir -p /data/pyfinder

docker stop mongo
docker rm mongo

docker run --name=mongo -v /data/pyfinder:/data/db -d mongo

IP="$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' mongo)"

echo "started mongo db on $IP..."
