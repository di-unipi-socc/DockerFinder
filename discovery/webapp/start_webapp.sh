#!/usr/bin/env bash

#google-chrome --disable-web-security &

#npm start
 #-p 8080

docker rm webapp
docker run --net=core-net --name=webapp  -p 80:80 --rm -v /home/dido/github/DockerFinder/discovery/webapp:/code dofinder/webapp:latest



#docker run --network=isolated_nw -itd --name=container3 busybox
