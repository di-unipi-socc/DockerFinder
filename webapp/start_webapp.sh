#!/usr/bin/env bash

#google-chrome --disable-web-security &

#npm start
 #-p 8080
docker run --net=core-net --name=webapp  -p 8080:8080 --rm -v /home/dido/github/DockerFinder/webapp:/code dofinder/webapp:latest



#docker run --network=isolated_nw -itd --name=container3 busybox
