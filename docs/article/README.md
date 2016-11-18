# Docker Finder

The new architecture of Docker Finder.

![achitecture](../architecture.png)

<!-- <div align="center">
<img src="../architecture.png" width="500">
</div> -->


The main additions are the following:

  1. `Management part`: contains the services for monitoring and management of the architecture.
      - `monitor`: is a Web service that is used to monitor the microservices running within the architecture.
      - `scaleScanner.py`: scales the number of scanners based on the load of the queue (it gets the load of the queue interacting with the monitor web service.)


  2. `Crawler` filters the images before sending them to the queue. It sends the images' name to the rabbitmq queue only if:
    - the image is new into local database, or
    - the image has been already scanned but it must be updated the description.

  3. `Checker` service in the `analysis part`. It performs two main tasks looking within the images database:
      - Remove the images that are not present into the docker Hub
      - Requeues the images if they have to be scanned again.
