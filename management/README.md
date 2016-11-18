# Management part


## Monitor Web Service

`Monitor` is a RESTful web service written in `python` using `flask`.

Th goal of the Web Service is to monitor and manage the microservices running within the `DockerFinder` infrastructure.


#### Monitor Api

Monitor exposes a RESTful API on port `3002`.

The API exposed permits to monitor any service in the architecture (up to now only the rabbitmq).

```
/service/<servicename>

```
For example:

```
GET http://127.0.0.1:3002/service/rabbitmq/queue/images

```
It returns queue `images` inforamtions of the `rabbitmq` service.


```
{
  "err": false,
  "load": 74,
  "queue": "images",
  "service": "rabbitmq"
}
```
The queue `iamges` in the `rabbitmq` service has `74` messages.


## Auto-scaling the scanners
The module `scaleScanners.py` is a client of the RESTful monitor web service.


It scales automatically the number of scanners based on the load of the queue of the rabbitMQ message broker.

The high level code of the auto-scaling scanner.
```
Every T seconds:
  load = get the number of messages in the queue # calling Monitor Web service
  # scale the scanners based on the load:
   if load < 100:  scale scanner  = 5
   elif load < 500: scale  scanner = 10
   elif load < 1000: scale scanner = 30
   else scale scanner = 40
```

The scanners are scaled in two type of environments:
  - `$ docker-compose scale SERVIE=REPLICAS` if the architecture is deployed in a single host with Docker- compose.
  - `$docker service scale SERVICE=REPLICAS` if the architecture is deployed in a distributed infrastructure using the `Docker 1.12` in swarm mode.
