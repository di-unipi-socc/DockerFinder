#!/usr/bin/env bash


# push test images
# docker run  --rm  --net=core-net  dofinder/crawler:latest push testImages  --amqp-url amqp://guest:guest@180.0.0.8:5672 --ex=dofinder --key=iamges.tests  --queue=test


docker run  --rm  --net=core-net  dofinder/crawler:latest crawl --amqp-url=amqp://guest:guest@180.0.0.8:5672 \
            --queue=images --fp=100 --ps=10 --mi=100

