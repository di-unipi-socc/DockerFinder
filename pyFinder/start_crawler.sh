#!/usr/bin/env bash





docker run  --rm  --net=core-net  dofinder/crawler:latest crawl --rmq=rabbitmq --queue=dofinder --fp=1 --ps=10 --mi=100