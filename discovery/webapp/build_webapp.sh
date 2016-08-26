#!/usr/bin/env bash


docker rmi dofinder/webapp

docker build -t dofinder/webapp --file Dockerfile .