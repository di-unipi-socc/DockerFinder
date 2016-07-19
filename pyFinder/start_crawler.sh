#!/usr/bin/env bash


docker rmi dofinder/crawler

docker build -t dofinder/crawler --file Dockerfile_crawler .

docker run  --rm  --net=core-net  dofinder/crawler:latest crawl --rmq=rabbitmq --queue=dofinder --fp=1 --ps=10 --mi=100