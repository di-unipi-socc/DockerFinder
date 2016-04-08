# DockerFinder

**Docker Registry** is a stateless, highly scalable server side application that
stores and lets you manage your own Docker images.


**Docker Hub** is a public registry maintained by Docker. It contains images you can download and
use to build containers. It provides authentication, work group structure, private repository for
storing images you don't want to share publicly.

*Command line* interface provide the `search` utility that search in the Docker Hub:

``` $ docker search [OPTIONS] TERM ```

Search the Term on different search fields:
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

## Build the description

The steps in order to build the description for the images :
1. Create a local Registry.
2. Download all the images in the DockerHub.
3. For all the images downloaded create a database with more information.

### Description structure
The description of the images can be decomposed in two main classes:
- information related to the Docker Hub description.
- information generated dynamically from the images.

The databases includes the tables
  - IMAGES(ID_IMAGE, name, star,tag)
  - LAYER(ID_LAYER,NAME)
  - IMALAYER(ID_IMAGES,ID_LAYER)
  - COMPONENETS(ID_COMP,name)
  - IMACOMP(ID_IMAGE, ID_COMP);
  

The structure can be a JSON file:

```
{
  "name":<image_name>
  "ID":<id>
  "tag":<tag>
  "size":<size>
  "stars": <number_Stars>
  "layer":
    [{
      "ID":<id>
      },
    ]

}
```
