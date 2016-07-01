#!/bin/bash

echo "Running the mongo db"
docker stop mongo &
docker run mongo &
nodemon . 
