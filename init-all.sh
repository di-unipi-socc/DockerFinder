#!/usr/bin/env bash



NET="core-net"

if docker network ls | grep -q $NET ; then
    echo $NET already exist
else
    echo $NET not found
    echo $(docker network create -d bridge --subnet 180.0.0.0/24 $NET)

fi


echo "Analysis part is starting ..."
#cd analysis &&  docker-compose up -d && cd ..  &



echo "Software service is starting ..."
#cd discovery/software_server && docker-compose up -d && cd .. &

echo "Web app  is starting ..."
cd discovery/webapp && ./start_webapp.sh  && cd .. &

echo "Storage part is starting ..."
cd storage &&  docker-compose up -d && cd ..  &



