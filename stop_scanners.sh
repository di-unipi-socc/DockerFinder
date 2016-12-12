#!/bin/sh
#for SERVICE in  ;do
#MAX_SCANNERS=8
#for i in `seq 1 $MAX_SCANNERS`;
#do
#  docker stop scanner$i
#  docker rm scanner$i
#done

docker service rm scanner
