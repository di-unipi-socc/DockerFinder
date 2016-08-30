#!/usr/bin/env bash



#docker run -v /var/run/docker.sock:/var/run/docker.sock  --restart=on-failure:5  --net=core-net dofinder/scanner:latest run  \
#                                                         --images-url=http://images_server:3000/api/images  \
#                                                         --queue=images --key=images.scan \
#                                                         --software-url=http://software_server:3001/api/software

#docker run -v /var/run/docker.sock:/var/run/docker.sock  --rm  --net=core-net  dofinder/scanner:latest pull official


## TEST SCANNER IAMGES
# docker run -v /var/run/docker.sock:/var/run/docker.sock  --restart=on-failure:5  --net=core-net dofinder/scanner:latest run  \
#                                                         --images-url=http://images_server:3000/api/images  \
#                                                         --queue=test --key=images.test \
#                                                         --software-url=http://software_server:3001/api/software \
#							 --rmi
#
#


docker-compose up scanner