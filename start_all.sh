#!/usr/bin/env bash

NET="docker-finder"
HUB_REPOSITORY=diunipisocc/docker-finder

#####################################################
###############   DISCOVERY PHASE ####################
#####################################################

# Software Database mongo
docker service create --network $NET --name software_db  \
  --constraint 'node.hostname==manager' \
  --mount type=volume,source=software-volume,destination=/data/software,volume-label="color=red" \
  mongo:3

# Software server
docker service create --network $NET  --name software_server  -p 3001:3001  \
  --constraint  'node.hostname==manager' \
  $HUB_REPOSITORY:software_server

###################################################
###############   STORAGE PHASE ####################
#####################################################

# Images database
docker service create --network $NET --name images_db  \
  --constraint  'node.hostname==manager' \
  --mount type=volume,source=images-volume,destination=/data/images,volume-label="color=red" \
  mongo:3

# Images software_server
docker service create --network $NET   --name images_server  \
    --constraint  'node.hostname==manager' \
    -p 3000:3000 $HUB_REPOSITORY:images_server

#####################################################
###############   ANALYSIS PHASE ####################
#####################################################

# RabbitMQ service
docker service create --network $NET --name rabbitmq \
  --constraint  'node.hostname==manager' \
  --mount type=volume,source=rabbit-volume,destination=/var/lib/rabbitmq,volume-label="color=red" \
  -p  8082:15672 rabbitmq:3-management


# Crawler service
docker service create  --network $NET  --name crawler \
  --constraint  'node.hostname==manager' \
  $HUB_REPOSITORY:crawler crawl  \
  --amqp-url=amqp://guest:guest@rabbitmq:5672  \
  --queue=images --fp=100 --ps=10 --mi=100

# Scanner service
#http://192.168.99.100:3001/api/software
# docker service create --network $NET finder --name scanner  \
#         --mount type=bind,source=/var/run/docker.sock,destination=/var/run/docker.sock \
#          diunipisocc/docker-finder:scanner run \
#         --images-url=http://images_server:3000/api/images  \
#         --queue=images  --key=images.scan  \
#         --software-url=http://software_server:3001/api/software --rmi

docker service create  --network $NET  --name scanner  \
      --mount type=bind,source=/var/run/docker.sock,destination=/var/run/docker.sock \
       $HUB_REPOSITORY:scanner run \
      --images-url=http://images_server:3000/api/images  \
      --queue=images  --key=images.scan  \
      --software-url=http://192.168.99.100:3001/api/software  --rmi
