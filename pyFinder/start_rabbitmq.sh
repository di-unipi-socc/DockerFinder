#!/usr/bin/env bash


docker stop rabbit

docker rm rabbit



# docker run -d --hostname my-rabbit --name some-rabbit -p 8080:15672 rabbitmq:3-management
# --hostname my-rabbit: is the hostname of the node running the rabbitMQ:
#                      connect to then node: rabbit@my-rabbit
# --name some-rabbit : is only the name of the container

docker run -d --hostname my-rabbit --name rabbitMq -p 8081:15672 --net core-net rabbitmq:3-management

# In order to run an app that comunicate with rabbitMq ( into default net)
# docker run --name some-app --link some-rabbit:rabbit -d application-that-uses-rabbitmq


IP="$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' rabbitMq)"

echo "RabbitMQ is running on $IP ..."

# connect to the application docker
# docker run --name some-app --link some-rabbit:rabbit -d application-that-uses-rabbitmq
