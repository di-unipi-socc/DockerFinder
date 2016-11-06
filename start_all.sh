#!/usr/bin/env bash
NET=docker-finder
HUB_REPOSITORY=diunipisocc/docker-finder

#for SERVICE in crawler scanner software_server ; do
  #-e affinity:container==frontend
  #docker service create --network $NET --name $SERVICE $HUB_REPOSITORY:$SERVICE
# start cralwer service
docker service create --network docker-finder --name crawler diunipisocc/docker-finder:crawler crawl --amqp-url=amqp://guest:guest@rabbitmq:5672 --queue=images --fp=100 --ps=10 --mi=100

# start scanner service
docker service create --network docker-finder --name scanner diunipisocc/docker-finder:scanner \
run --images-url=http://images_server:3000/api/images --queue=images     \
--key=images.scan --software-url=http://software_server:3001/api/software --rmi \


#done
