#!/usr/bin/env bash

NET="docker-finder"
HUB_REPOSITORY=diunipisocc/docker-finder

#####################################################
###############   DISCOVERY PHASE ####################
#####################################################

# Software Database mongo
docker service create --network $NET --name software_db  \
  --mount type=volume,source=software-volume,destination=/data/software,volume-label="color=red" \
  mongo:3

# Software server
docker service create --network $NET  --name software_server  -p 3001:3001 diunipisocc/docker-finder:software_server

###################################################
###############   STORAGE PHASE ####################
#####################################################

# Images database
docker service create --network $NET --name images_db  \
  --mount type=volume,source=images-volume,destination=/data/images,volume-label="color=red" \
  mongo:3

# Images software_server
docker service create --network $NET   --name images_server  -p 3000:3000 diunipisocc/docker-finder:images_server

#####################################################
###############   ANALYSIS PHASE ####################
#####################################################

# RabbitMQ service
docker service create --network $NET --name rabbitmq \
  --mount type=volume,source=rabbit-volume,destination=/var/lib/rabbitmq,volume-label="color=red" \
  -p  8082:15672 rabbitmq:3-management

# rabbitmq:
#   image: rabbitmq:3-management
#   hostname: rabbitmq
#   restart: on-failure:3
#   restart: always
#   #container_name: rabbitmq
#   ports:
#     - 8082:15672
#   volumes:
#     - /var/lib/rabbitmq
#   networks:
#      - docker-finder
# Crawler service
docker service create --network docker-finder --name crawler diunipisocc/docker-finder:crawler crawl  \
        --amqp-url=amqp://guest:guest@rabbitmq:5672  \
        --queue=images --fp=100 --ps=10 --mi=100

# Scanner service
#http://192.168.99.100:3001/api/software
docker service create --network docker-finder --name scanner  \
        --mount type=bind,source=/var/run/docker.sock,destination=/var/run/docker.sock \
         diunipisocc/docker-finder:scanner run \
        --images-url=http://images_server:3000/api/images  \
        --queue=images  --key=images.scan  \
        --software-url=http://software_server:3001/api/software --rmi

docker service create --network docker-finder --name scanner  \
      --mount type=bind,source=/var/run/docker.sock,destination=/var/run/docker.sock \
       diunipisocc/docker-finder:scanner run \
      --images-url=http://images_server:3000/api/images  \
      --queue=images  --key=images.scan  \
      --software-url=http://192.168.99.100:3001/api/software  --rmi
