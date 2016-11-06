#!/usr/bin/env bash


#docker network create --driver overlay dockercoins
NET="docker-finder"

if docker network ls | grep -q $NET ; then
    echo $NET network already exist.
else
    echo $NET network not found.
    echo $(docker network create --driver overlay  --subnet 192.168.0.0/24 $NET)
    #echo $(docker network create -d bridge --subnet 180.0.0.0/24 $NET)

fi

# build and push the images  into Docker Registry
HUB_REPOSITORY=diunipisocc/docker-finder
#TAG=v0.1
echo "Build and publish the images ..."
for SERVICE in  software_server images_server scanner crawler ;do # is built on a image
  docker-compose build $SERVICE
  docker tag dockerfinder_$SERVICE $HUB_REPOSITORY:$SERVICE
  docker push $HUB_REPOSITORY:$SERVICE
  echo "  Pushed:  $HUB_REPOSITORY:$SERVICE"
done

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
