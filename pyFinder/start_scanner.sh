#!/usr/bin/env bash

docker rmi dofinder/scanner

docker build -t dofinder/scanner --file Dockerfile_scanner .

docker run -v /var/run/docker.sock:/var/run/docker.sock  --rm  --net=core-net  dofinder/scanner:latest run
