#!/usr/bin/env bash

docker rmi -f dofinder/scanner

docker build -t dofinder/scanner dock--file Dockerfile_scanner .