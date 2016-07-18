

# DockerFinder

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Thesis](#thesis)
  - [regex](#regex)
- [PyFinder](#pyfinder)
- [ServerApi](#serverapi)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->



# Thesis
1.  Identify th useful informations and describe the features od the images,
and defines a model that describe that informations.
2. Defines how to extract the information starting from a **Docker image** or a **Docker file**.
3. Develops a intelligent **search system** that is able to identify the images that
offer determined features and not only based on the name and the tag.

  
### Description
The description of the images can be decomposed in:
- information related to the `Docker Hub description`.
- information generated dynamically from the `images` (running scrips inside the containers)
- information from the `Docker file`.


### regex 
This regex extract the version number of the form `number.number[number | letters]` 
 
`[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*`


```
import re
regex = re.compile('[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*')
match = regex.search("python 3.3.4.")
match.group(0)

```

# PyFinder
In order to collect the description from the images, i have found a
[docker-py](https://github.com/docker/docker-py)  that is a Python library  that expose all the docker commnad. Can be useful to run an images directly into a python code.




### Docker crawler
The *crawler* is a python class that crawl from the docker Hub all the images name.


<div style="text-align:center">
<img src="https://cloud.githubusercontent.com/assets/9201530/15286937/e62ac2a6-1b5f-11e6-97d4-9a01d5d135ac.png" width="500">
</div>
  
## RabbitMQ server 
The rabbit MQ runs in a docker container.


```
docker run -d --hostname my-rabbit --name rabbitMq -p 8081:15672 --net core-net rabbitmq:3-management
```

- *--hostname* my-rabbit: is the hostname of the node running the rabbitMQ:
         connect to then node: rabbit@my-rabbit
- *--name* some-rabbit : is only the name of the container

- *client_dockerhub.py* is the module that parforms the requests to the docker hub.
- The crawler is a *rabbotMQ* client. It sends into the channel the  name of th eimages found.


#### Docker HUB crawling

```
  next = 1
  while(next != nul){
      10image = send GET to https://hub.docker.com/v2/search/repositories/?page=NUMBER&query=* 
      add the info into the database      
      next = 10.image['next']     //null if is the last page
  }
```

the previous call return:
```
{
  "count": 299569,
  "next": "https://hub.docker.com/v2/search/repositories/?query=%2A&page=29957",
  "previous": "https://hub.docker.com/v2/search/repositories/?query=%2A&page=29955",
  "results": [
    {
      "star_count": 0,
      "pull_count": 236,
      "repo_owner": null,
      "short_description": " ",
      "is_automated": true,
      "is_official": false,
      "repo_name": "jess/audacity"
    },
    [{}]
    ...
}
```


#### Docker API v1

- **search**:
  ```
  GET v1/search?q=search_term&page=1&n=25 HTTP/1.1
  Host: index.docker.io
  Accept: application/json

  ```

  where the query parameters are:
  
  - **q** : the TERM that  you want to search.
  - **n** :the number of results per page (default: 25, min:1, max:100)
  - **page**: page number of results.

Example response of previous GET:
 ```
      HTTP/1.1 200 OK
     Vary: Accept
     Content-Type: application/json

     {"num_pages": 1,
       "num_results": 3,
       "results" : [
          {"name": "ubuntu", "description": "An ubuntu image..."},
          {"name": "centos", "description": "A centos image..."},
          {"name": "fedora", "description": "A fedora image..."}
        ],
       "page_size": 25,
       "query":"search_term",
       "page": 1
      }
  ````



#### Docker Registry HTTP API V2.
[distribution gitHub](https://github.com/docker/distribution)
[registry](https://docs.docker.com/registry/overviw)
Goals.

    - simplicity
    - distribution (saparation of content fro namenig)
    - security (veriable iamges)
    - performance  
    - implementatian (move to Go)

**digest**: uniquely identify content (each layer is a content-addressable blob, Sha256)

**Manifest** describes the component of an image ina single object (layers can be fetched in parallel)
```docker pull ubuntu@sha256orgihgoiaeho...```
*Tags* are in the manifest.

**Repository**
 
 V1 vs V2 AI
 - content addresses (digest) are primary identifiers
 - no search API (reaplaced with somthing better)
 - no explicit tagging API
 
 
#### Athentication 
```
GET https://auth.docker.io/token?service=registry.docker.io&scope=registry:catalog:*

```

return a jason token 
```
{
token: "TOKEN"
}
```

`https://registry-1.docker.io/v2/dido/webofficina/tags/list`

Use the token to submit the operation (check if end point ha version 2)
```
GET https://index.docker.io/v2/

Authorization: Bearer TOKEN 
```



# ServerApi

### Server API 
All the request for the api must be prefixed by `/api` anr `Content-Type: application\json`

- `GET /images` : get all the images of the database
    - `GET /images/?select=repo_name%20bins`
    - `GET /images/?sort=repo_name` : get all the images sorted by repo_name
- `POST /images`: create a new image from the json in the body
-  `PUT /images/:id_image`: update the image
- `DELETE /iamges/:id_image`: delete the image.



## Elastic search 


- [stack overlflow](http://stackoverflow.com/questions/29841348/how-reliable-is-elasticsearch-as-a-primary-datastore-against-factors-like-write): it is correct to use elstic search as  primary data store..
- [elasticsearch](https://www.elastic.co/guide/en/elasticsearch/resiliency/current/index.html): official documentatio
