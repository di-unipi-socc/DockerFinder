#!/usr/bin/env bash


#docker build -t dofinder/scanner --file ./Dockerfile_scanner .

# --name scanner1

docker run -v /var/run/docker.sock:/var/run/docker.sock  --rm  --net=core-net  dofinder/scanner:latest run
