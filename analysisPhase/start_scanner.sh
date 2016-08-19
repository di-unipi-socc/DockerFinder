#!/usr/bin/env bash


# Combining --restart (restart policy) with the --rm (clean up) flag results in an error.
#docker run -v /var/run/docker.sock:/var/run/docker.sock  --restart=on-failure:5  --net=core-net  dofinder/scanner:latest run
docker run -v /var/run/docker.sock:/var/run/docker.sock  --restart=on-failure:5  --net=core-net dofinder/scanner:latest run  \
                                                         --images-url=http://images_server:3000/api/images  \
                                                         --queue=images --key=images.scan \
                                                         --software-url=http://sw_server:3001/api/software
#docker run -v /var/run/docker.sock:/var/run/docker.sock  --rm  --net=core-net  dofinder/scanner:latest pull official
