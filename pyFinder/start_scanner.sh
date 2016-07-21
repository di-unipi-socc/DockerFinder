#!/usr/bin/env bash


# Combining --restart (restart policy) with the --rm (clean up) flag results in an error.
docker run -v /var/run/docker.sock:/var/run/docker.sock  --restart=on-failure:5  --net=core-net  dofinder/scanner:latest run

#docker run -v /var/run/docker.sock:/var/run/docker.sock  --rm  --net=core-net  dofinder/scanner:latest pull official
