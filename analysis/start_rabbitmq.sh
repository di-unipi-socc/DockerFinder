#!/usr/bin/env bash


docker service create --network docker-finder --name rabbitmq rabbitmq:3-management
