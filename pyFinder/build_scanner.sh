#!/usr/bin/env bash

docker rmi dofinder/scanner

docker build -t dofinder/scanner --file Dockerfile_scanner .