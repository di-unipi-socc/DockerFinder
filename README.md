# DockerFinder
Steps of the thesis:
1.  Identify th useful informations and describe the features od the images,
and defines a model that describe that informations.
2. Defines how to extract the information starting from a **Docker image** or a **Docker file**.
3. Develops a intelligent **search system** that is able to identify the images that
offer determined features and not only based on the name and the tag.


Next steps to be performed:
  - decide the structure of the inforamation (relational DB ?? )
  - Write the scripts in order to indentify the capability of the images.
  - starting from docker file ,generate the informations.

# regex 
This regex extract the version number of the form `number.number[number | letters]` 
 
`[0-9]\.[0-9](\.[0-9])*[^\s]*`


```
import re
p = re.compile('[0-9]\.[0-9](\.[0-9])*[^\s]*')
p = p.search("python 3.3.4.")
p.group(0)

```


### Description
The description of the images can be decomposed in:
- information related to the `Docker Hub description`.
- information generated dynamically from the `images` (running scrips inside the containers)
- information from the `Docker file`.


### Collects the description
In order to collect the description from the images, i have found a
[docker-py](https://github.com/docker/docker-py)  that is a Python library  that expose all the docker commnad. Can be useful to run an images directly into a python code.


There are two possiblities to implement the thesi:

1. **docker finder**:
    -  Create a local Registry.
    -  Download all the images from the DockerHub (create a copy).
    -  Create a database with more useful information for all the images downloaded.

2. **docker on-line description** :
    - expose a service, input: docker image or docker file.
    - download the images from ducker.hub
    - generates the description of the image.
    - sends the description to the user
<div style="text-align:center">
<img src="https://cloud.githubusercontent.com/assets/9201530/15286937/e62ac2a6-1b5f-11e6-97d4-9a01d5d135ac.png" width="500">
</div>
    

###  Docker registries
Docker provides two kind of registries:

1. **Docker Registry** is a stateless, highly scalable server side application that
stores and lets you manage your `own` Docker images.

2. **Docker Hub** is a public registry maintained by Docker. It contains images you can download and
use to build containers. It provides authentication, work group structure, private repository for
storing images you don't want to share publicly.

### Docker search
Docker provides through the *Command line* the `search` utility that search in the Docker Hub. The sysntax is of the form:

``` $ docker search [OPTIONS] TERM ```

Term is searched in all the fields:
- **image name** (top-level namespace of official repository does not show the repository `reposUser/imagesNmae`).
- **user name**.
- **description** (match also substring in the description)

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
 
 
##### Atherntication 
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

###Mongo Schemas

Information from  `docker inspect INAME_NAME`
```
{  "_id" : SHA256_IMAGE
   "RepoTags": [ TAGS_IMAGE ]
   
   
   "RootFS": {
            "Type": "layers",
            "Layers": [
                "sha256:4dcab49015d47e8f300ec33400a02cebc7b54cadd09c37e49eccbc655279da90"
            ]
        }
}
```

Information from `docker search IMAGE_NAME`
```
{
    "Stars": NUMBER,
    "Official": "YES/NO"
}
```
Information from `doFinder NAME_IMAGE`

```
  "System": { "Distro": NAME_DISTRO
             }
  "Bins": [ 
           {"Bin": NAME_BINARY
            "Ver": VERSION},
        ]
```


final description of one image

```
{  "_id" : SHA256_IMAGE
   "RepoTags": [ TAGS_IMAGE ]
   "RootFS": {
            "Type": "layers",
            "Layers": [
                "sha256:4dcab49015d47e8f300ec33400a02cebc7b54cadd09c37e49eccbc655279da90"
            ]
        },
   "Stars":NUMBER,
   "Official": "YES/NO"
   
   
}



```
