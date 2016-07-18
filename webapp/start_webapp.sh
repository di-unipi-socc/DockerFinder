#!/usr/bin/env bash

#google-chrome --disable-web-security &

#npm start
docker run --net=core-net --name=webapp  --rm -v /home/dido/github/DockerFinder/webapp:/code  -p 80 dofinder/webapp:latest



#docker run --network=isolated_nw -itd --name=container3 busybox
