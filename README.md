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

    [Docker on-line description](https://www.dropbox.com/s/j1dcuvgmu3l0ttn/Docker.pdf?dl=0 )

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
Introduce the image **manifest**  : semplifies images definition and improves security.

- authentication (OAuth2).
- Layering information
- SHA256 on layer ID and Data.

