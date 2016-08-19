
#!/usr/bin/env bash

docker rmi -f dofinder/crawler

docker build -t dofinder/crawler --file Dockerfile_crawler .
