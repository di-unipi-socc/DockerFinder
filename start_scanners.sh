#!/bin/sh

IP_MANAGER=131.114.106.31


#for SERVICE in  ;do
MAX_SCANNERS=8

for i in `seq 1 $MAX_SCANNERS`;
do
  docker run -d -v /var/run/docker.sock:/var/run/docker.sock --name scanner$i \
          diunipisocc/docker-finder:scanner run \
          --images-url=http://$IP_MANAGER:3000/api/images/  \
          --amqp-url=amqp://guest:guest@$IP_MANAGER:5672 --queue=images --key=images.scan \
          --software-url=http://$IP_MANAGER:3001/api/software \
           --rmi &
done
#done

#         docker run -v /var/run/docker.sock,destination=/var/run/docker.sock  \
#                 diunipisocc/docker-finder:scanner run \
#                 --images-url=http://127.0.0.1:3000/api/images/  \
#                 --amqp-url=amqp://guest:guest@127.0.0.1:5672 --queue=images --key=images.scan \
#                 --software-url=http://127.0.0.1:3001/api/software \
#                  --rmi
