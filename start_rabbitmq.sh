#!/usr/bin/env bash


docker stop rabbit

docker rm rabbit

docker run -d --hostname my-rabbit --name rabbit rabbitmq:3

IP="$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' rabbit)"

echo "RabbitMQ is running on $IP ..."