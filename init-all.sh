#!/usr/bin/env bash


# create folder for checker log 
mkdir -p /dockerfinder/checker/log

#docker network create --driver overlay dockercoins
NET="docker-finder"

if docker network ls | grep -q $NET ; then
    echo $NET network already exist.
else
    echo $NET network not found.
    docker network create --driver overlay  $NET
    echo "OVerlay Network ceated " $NET
    #echo $(docker network create -d bridge --subnet 180.0.0.0/24 $NET)

fi

# build and push the images  into Docker Registry
HUB_REPOSITORY=diunipisocc/docker-finder
#TAG=v0.1
echo "Build and publish the images ..."
for SERVICE in software_server images_server scanner crawler monitor checker ;do #scale_scanner;do # is built on a image
  docker-compose build $SERVICE > /dev/null
  docker tag dockerfinder_$SERVICE $HUB_REPOSITORY:$SERVICE > /dev/null
  docker push $HUB_REPOSITORY:$SERVICE > /dev/null
  if [ $? -eq 0 ]
  then
    echo "Created and Pushed:  $HUB_REPOSITORY:$SERVICE"
  else
    echo "Could not create $HUB_REPOSITORY:$SERVICE" >&2
    exit 1
  fi
done


# echo "Creating Manager Node ..."
# e = $(docker-machine  create  --driver virtualbox manager)
#
#
# TOKEN=$(docker swarm join-token -q manager)
#
# for N in 1 2; do
#   eval $(docker-machine env worker$N)
#   docker swarm join --token $TOKEN manager:2377
#   echo "worker$N : added mnafger token..."
# done

# assign type to the master node
#docker node update --label-add type=master didoUbuntu


#echo "Analysis part is starting ..."
#cd analysis &&  docker-compose up -d && cd ..  &

#echo $(docker service create --network $NET --name rabbitmq rabbitmq:3-management)
#echo "   RabbitMq service created"


#echo "Software service is starting ..."
#echo $(docker service create --network $NET --mount type=volume,destination=/data/db --name mongo mongo:3)
#cd discovery/software_server && docker-compose up -d && cd .. &

#echo "Web app  is starting ..."
#cd discovery/webapp && ./start_webapp.sh  && cd .. &

#echo "Storage part is starting ..."
#cd storage &&  docker-compose up -d && cd ..  &
