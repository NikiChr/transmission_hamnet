#!/bin/bash

docker pull nikitach/babeld:latest
docker tag nikitach/babeld:latest localhost:5000/babeld
docker push localhost:5000/babeld

docker pull registry:2.7.1
docker tag registry:2.7.1 localhost:5000/registry
docker push localhost:5000/registry

docker pull linuxserver/transmission
docker tag linuxserver/transmission:latest localhost:5000/transmission
docker push localhost:5000/transmission

docker pull lednerb/opentracker-docker
docker tag lednerb/opentracker-docker:latest localhost:5000/opentracker-docker
docker push localhost:5000/opentracker-docker

docker build -t transmission_stage1 .
docker run --privileged -d --name transmission_build transmission_stage1
sleep 10
docker exec transmission_build docker-compose up --no-start
sleep 10
docker stop transmission_build
docker commit transmission_build transmission_dind
docker rm transmission_build
echo '***Image transmission_dind erstellt!'

#docker build -t kraken_dind .