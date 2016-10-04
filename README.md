

# DockerFinder

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE 
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Thesis](#What is Docker Finder ?)
  - [regex](#regex)
- [PyFinder](#pyfinder)
- [ServerApi](#serverapi)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->
**Enhanced discovery of Docker
images**  is the title thesis submitted for the degree of
MSc in Computer Science and Networking
University of Pisa and SSSUP Sant’Anna. a.a. 2015/2016


## What is Docker Finder ?
Docker Finder is a tool enabling a more powerful search of Docker images with
respect to the tools currently provided by the Docker platform (**docker search**, **Docker Hub**).

The main steps performed by Docker Finder are the following

1. Download Docker images from the Docker Hub,
2. generate and store a new description of the images into a local storage,
and
3. search the images by looking into the Docker Finder description storage.

## GUI of Docker Finder
<div style="text-align:center">
<img src="./docs/df_gif.gif" width="500">
</div>

## Docker Finder-in-Docker
The figure represents the architecture of Docker Fidner deployed with the Docker platform.

<div style="text-align:center">
<img src="./docs/architecture_docker.png" width="500">
</div>
 
