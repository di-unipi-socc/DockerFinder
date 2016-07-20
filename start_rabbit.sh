#!/usr/bin/env bash

#docker run --rm --net=core-net --hostname rabbitmq --name rabbitmq -p 8081:15672 rabbitmq:3-management
#-v <log-dir>:/data/log   --name rabbitmq
#  /var/lib/rabbitmq/mnesia/
docker stop rabbitmq
docker rm rabbitmq
docker run  --net=core-net -v /data/rabbit:/var/lib/rabbitmq/mnesia/ --hostname rabbitmq  --name rabbitmq -p 8081:15672 rabbitmq:3-management
