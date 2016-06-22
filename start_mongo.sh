#!/bin/bash


mkdir -p ~/mongo/

docker run -v /home/dido/github/DockerFinder/mongo:/data/db -d mongo

echo "started  mongo db, store in /home/dido/github/DockerFinder/mongo ..."
