#!/usr/bin/env bash

# create folder for checker log
mkdir -p /dockerfinder/checker/log

# create machine locally

#docker network create --driver overlay dockercoins
# NET="docker-finder"
#
# if docker network ls | grep -q $NET ; then
#     echo $NET network already exist.
# else
#     echo $NET network not found.
#     docker network create --driver overlay  $NET
#     echo "OVerlay Network ceated " $NET
#     #echo $(docker network create -d bridge --subnet 180.0.0.0/24 $NET)
#
# fi

# # build and push the images  into Docker Registry
# HUB_REPOSITORY=diunipisocc/docker-finder
# #TAG=v0.1
# echo "Build and publish the images ..."
# for SERVICE in software_server images_server scanner crawler monitor checker ;do #scale_scanner;do # is built on a image
#   docker-compose build $SERVICE > /dev/null
#   docker tag dockerfinder_$SERVICE $HUB_REPOSITORY:$SERVICE > /dev/null
#   docker push $HUB_REPOSITORY:$SERVICE > /dev/null
#   if [ $? -eq 0 ]
#   then
#     echo "Created and Pushed:  $HUB_REPOSITORY:$SERVICE"
#   else
#     echo "Could not create $HUB_REPOSITORY:$SERVICE" >&2
#     exit 1
#   fi
# done
################################
managers=1
workers=2

MANAGER_NODE_NAME=swarm-manager
HOST_NODE_NAME=worker

# create manager machines
echo "======> Creating $MANAGER_NODE_NAME manager machines ...";
docker-machine create -d virtualbox $MANAGER_NODE_NAME;


if [ $(docker-machine status $MANAGER_NODE_NAME) == "Stopped" ]; then
	echo "====> Restarting node $MANAGER_NODE_NAME "
	docker-machine restart $MANAGER_NODE_NAME
fi


# create worker machines
echo "======> Creating $workers worker machines ...";
for node in $(seq 1 $workers);
do
	echo "======> Creating $HOST_NODE_NAME-$node machine ...";
	docker-machine create -d virtualbox $HOST_NODE_NAME-$node ;
	if [ $(docker-machine status $HOST_NODE_NAME-$node) == "Stopped" ]; then
		echo "====> Retarting node $HOST_NODE_NAME-$node"
		docker-machine restart $HOST_NODE_NAME-$node
	fi
done

# list all machines
docker-machine ls

# initialize swarm mode and create a manager
echo "======> Initializing first swarm manager ..."
X=$(docker-machine ssh $MANAGER_NODE_NAME "docker swarm init --listen-addr $(docker-machine ip $MANAGER_NODE_NAME) --advertise-addr $(docker-machine ip $MANAGER_NODE_NAME)")


# get manager and worker tokens
#export manager_token=`docker-machine ssh $MANAGER_NODE_NAME "docker swarm join-token manager -q"`
export worker_token=`docker-machine ssh $MANAGER_NODE_NAME "docker swarm join-token worker -q"`

#echo "manager_token: $manager_token"
echo "worker_token: $worker_token"

# # other masters join swarm
# for node in $(seq 2 $managers);
# do
# 	echo "======> manager$node joining swarm as manager ..."
# 	docker-machine ssh manager$node \
# 		"docker swarm join \
# 		--token $manager_token \
# 		--listen-addr $(docker-machine ip manager$node) \
# 		--advertise-addr $(docker-machine ip manager$node) \
# 		$(docker-machine ip manager1)"
# done

# # show members of swarm
# docker-machine ssh manager1 "docker node ls"

# workers join swarm
for node in $(seq 1 $workers);
do
	echo "======> $HOST_NODE_NAME-$node joining swarm as worker ..."
	docker-machine ssh $HOST_NODE_NAME-$node \
	"docker swarm join \
	--token $worker_token \
	--listen-addr $(docker-machine ip $HOST_NODE_NAME-$node) \
	--advertise-addr $(docker-machine ip $HOST_NODE_NAME-$node) \
	$(docker-machine ip $MANAGER_NODE_NAME):2377"
done

# show members of swarm
docker-machine ssh $MANAGER_NODE_NAME "docker node ls"

###############################
#
# # token for the swarm
# SWARM_CLUSTER_TOKEN="$(docker run swarm create)"
#
# echo "Swarm token: $SWARM_CLUSTER_TOKEN"
#
# MANAGER_NODE_NAME=swarm-manager
# HOST_NODE_NAME=worker
#
# if ! docker-machine ls -q | grep $MANAGER_NODE_NAME; then
#   echo "Creating $MANAGER_NODE_NAME ..."
#   #e = $(docker-machine  create --swarm --swarm-master --driver virtualbox manager )
#   docker-machine create \
#       -d virtualbox \
#       --swarm \
#       --swarm-master \
#       --swarm-discovery token://$SWARM_CLUSTER_TOKEN \
#       $MANAGER_NODE_NAME > /dev/null
#       if [ $? -eq 0 ]
#         then
#           echo "Created succesfully node: $MANAGER_NODE_NAME"
#         else
#           echo "Could not create $MANAGER_NODE_NAME" >&2
#           exit 1
#         fi
# else
#     echo "$MANAGER_NODE_NAME already exist."
# fi
#
# for N in 1 2; do
#   if ! docker-machine ls -q | grep $HOST_NODE_NAME-$N; then
#       echo "Creating $HOST_NODE_NAME-$N ..."
#         docker-machine create \
#             -d virtualbox \
#             --swarm \
#             --swarm-discovery token://$SWARM_CLUSTER_TOKEN \
#             "$HOST_NODE_NAME-$N"
#     else
#       echo "$HOST_NODE_NAME-$N already exist."
#     fi
# done
#
# #Point your Docker environment to the machine running the swarm master.
# eval $(docker-machine env --swarm $MANAGER_NODE_NAME)
#
# # # connect to manager node
# eval $(docker-machine env manager)
#
# # inital swarm in manager node
# docker swarm init --advertise-addr 192.168.99.100
#
# for N in 1 2; do
#   eval $(docker-machine create worker$N)
#   docker-machine creare  worker$N
#   echo "worker$N : added mnafger token..."
# don
#
# for N in 1 2; do
#   eval $(docker-machine env worker$N)
#   docker swarm join --token $TOKEN manager:2377
#   echo "worker$N : added mnafger token..."
# done
#
#
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
