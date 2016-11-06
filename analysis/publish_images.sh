#!/usr/bin/env bash

# build the images on push them into Docker Registry

HUB_REPOSITORY=diunipisocc/docker-finder
#TAG=v0.1

for SERVICE in  scanner crawler; do # rabbitmq is built on a image
  docker-compose build $SERVICE
  docker tag analysis_$SERVICE $HUB_REPOSITORY:$SERVICE
  docker push $HUB_REPOSITORY:$SERVICE
done



#
# # Scanner image
# docker build  -f ./Dockerfile_scanner -t diunipisocc/docker-finder:scanner .
# docker push diunipisocc/docker-finder:scanner
#
#
# # Scanner image
# docker build  -f ./Dockerfile_crawler -t diunipisocc/docker-finder:crawler .
# docker push diunipisocc/docker-finder:crawler
