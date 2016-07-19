#!/usr/bin/env bash

docker rmi dofinder/crawler

docker build -t dofinder/crawler --file Dockerfile_crawler .