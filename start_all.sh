#!/bin/sh


#if [ $1 -eq 'start' ] && [ $1 -eq 'create'] && [ $1 -eq 'update']; then
#  CMD = $1
#else:
#  exit 1
#fi

NET="docker-finder"
HUB_REPOSITORY=diunipisocc/docker-finder

#"${NODE_MANAGER?Set Manger node:  $ export NODE_MANAGER=<managernode>}"
if [ -z "$NODE_MANAGER" ]; then
    echo "NODE_MANAGER environment variable is not set"
    THISHOST=$(hostname)
    CONSTRAINT_NODE="node.hostname==$THISHOST"
    echo "Using Constraint: " $CONSTRAINT_NODE
else
    CONSTRAINT_NODE="node.hostname==$NODE_MANAGER"
    echo "Using Constraint: " $CONSTRAINT_NODE
fi



#####################################################
###############   DISCOVERY PHASE ####################
#####################################################
#if [ $2 -eq 'discover' ] || [ -z $2 ]; then
# Software Database mongo
SOFTWAREDB=software_db
docker service create --network $NET --name $SOFTWAREDB  \
  --constraint $CONSTRAINT_NODE \
  --mount type=volume,source=software-volume,destination=/data/software,volume-label="color=red" \
  mongo:3 > /dev/null
if [ $? -eq 0 ]
  then
    echo "$SOFTWAREDB:service created"
  else
    echo "Could not create $SOFTWAREDB service" >&2
    exit 1
fi

# Software server
SOFTWARE=software_server
docker service create --network $NET  --name $SOFTWARE -p 3001:3001  \
  --constraint  $CONSTRAINT_NODE \
  $HUB_REPOSITORY:software_server > /dev/null
  if [ $? -eq 0 ]
    then
      echo "$SOFTWARE: service created"
    else
      echo "Could not create $SOFTWARE service" >&2
      exit 1
  fi

###################################################
###############   STORAGE PHASE ####################
#####################################################

# Images database
docker service create --network $NET --name images_db  \
  --constraint  $CONSTRAINT_NODE \
  --mount type=volume,source=images-volume,destination=/data/images,volume-label="color=red" \
  mongo:3 > /dev/null
  if [ $? -eq 0 ]
    then
      echo "images_db:service created"
    else
      echo "Could not create images_db service" >&2
      exit 1
  fi


# Images software_server
docker service create --network $NET   --name images_server  \
    --constraint $CONSTRAINT_NODE \
    -p 3000:3000 $HUB_REPOSITORY:images_server  > /dev/null
if [ $? -eq 0 ]
    then
      echo "images_server service created"
    else
      echo "Could not create images_server service" >&2
      exit 1
fi

#####################################################
###############   ANALYSIS PHASE ####################
#####################################################

# RabbitMQ service
docker service create --network $NET --name rabbitmq \
  --constraint  $CONSTRAINT_NODE \
  --mount type=volume,source=rabbit-volume,destination=/var/lib/rabbitmq \
  -p  8082:15672 \
  rabbitmq:3-management   > /dev/null
if [ $? -eq 0 ]
      then
        echo "rabbitmq: service created"
      else
        echo "Could not create rabbitmq service" >&2
        exit 1
  fi

# Crawler service
docker service create  --network $NET  --name crawler \
  --constraint  $CONSTRAINT_NODE \
  --mount type=volume,source=crawler-volume,destination=/data/crawler \
  $HUB_REPOSITORY:crawler crawl  \
  --images-url=http://images_server:3000/api/images \
  --amqp-url=amqp://guest:guest@rabbitmq:5672  \
  --save-url=/data/crawler/lasturl.txt \
  --queue=images --fp=1 --ps=100   > /dev/null #--mi=100
  if [ $? -eq 0 ]
        then
          echo "crawler: service created"
        else
          echo "Could not create crawler service" >&2
          exit 1
    fi

# Scanner service
docker service create  --network $NET  --name scanner  \
      --mount type=bind,source=/var/run/docker.sock,destination=/var/run/docker.sock \
       $HUB_REPOSITORY:scanner run \
      --images-url=http://images_server:3000/api/images  \
      --queue=images  --key=images.scan  \
      --software-url=http://software_server:3001/api/software  --rmi  > /dev/null
if [ $? -eq 0 ]
    then
        echo "scanner: service created"
    else
        echo "Could not create scanner service" >&2
        exit 1
fi

#####################################################
###############   MONITOR PHASE ####################
#####################################################
docker service create  --network $NET  -p 3002:3002 --name monitor \
  --constraint  $CONSTRAINT_NODE \
  $HUB_REPOSITORY:monitor > /dev/null
  if [ $? -eq 0 ]
      then
          echo "monitor: service created"
      else
          echo "Could not create monitor service" >&2
          exit 1
  fi


#docker service ls
