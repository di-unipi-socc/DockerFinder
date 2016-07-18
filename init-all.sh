#!/usr/bin/env bash


docker network create -d bridge --subnet 180.0.1.0/24 images-net

docker network create -d bridge --subnet 180.0.2.0/24 webapp-net