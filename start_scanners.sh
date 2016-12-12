#!/bin/sh

#IP_MANAGER=131.114.106.31
MAX_SCANNERS=8

if [ -z "$IP_MANAGER" ]; then
    echo "IP_MANAGER environment variable is not set"
    echo "$ export IP_MANAGER=<ipaddress>"
    exit 1
else
    #IP_MANAGER=$IP_MANAGER
    echo "Manager node: " $IP_MANAGER
fi

MAX_SCANNERS=8

docker service create  --name scanner  \
      --mount type=bind,source=/var/run/docker.sock,destination=/var/run/docker.sock \
       diunipisocc/docker-finder:scanner  run \
      --images-url=http://$IP_MANAGER:3000/api/images/  \
      --amqp-url=amqp://guest:guest@$IP_MANAGER:5672 --queue=images --key=images.scan \
      --software-url=http://$IP_MANAGER:3001/api/software \
        --rmi  > /dev/null
if [ $? -eq 0 ]
    then
        echo "Scanner service created"
    else
        echo "Could not create scanner service" >&2
        exit 1
fi

docker service scale scanner=$MAX_SCANNERS
