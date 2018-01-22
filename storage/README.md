# Storage
DockerFinder stores all image descriptions produced by the
Scanners into a **local repository**, and it makes them accessible
to the other microservices in DockerFinder through a RESTful API.

```
Storage
|
|___images_server:
|   |___models
|   |   |___image.js: defines the model of an image's description
|   |___routes
|        |___api.js : the RESTful  API for the mansing the images
|        |___search.js: the search API for searching the images.
|
|____imagesManager.py: python script for PULL, UPLOAD or RM the imagee stored into the db
|
|____images-13gen-12250.js: set of 12250 images already analysed by DockerFinder
```

## JSON description of image in DockerFinder

An image is described by a JSON, where the most important information are listed below:
 - *id*: is the unique identifier of the image inside DockerFinder.
 - *name*: is the name of the image (repository:tag)
 - *stars*: number of stars received by the repository (not the image)
 - *pulls*: number of time an image is dowloade from the the repository.
 - *size*: size (in bytes) of the image ,
 - *distro*: name of the OS distribution (e.g., Ubuntu precise (12.04.5 LTS))
 - *last_scan*: datetime of the last scan performed by Docker Finder (e.g.,"2017-11-17T16:03:50.457Z",)
 - *last_updated*: datetime of the last time the image was updated in Docker Hub (e.g., "2017-04-24T22:59:38.213Z",)
 - *softwares*: list of the softwares versions supported by the image (e.g., Python 2.7)
 - "inspect_info": object eith the inspect information of an image:
      - *Id*: SHA256 as unique identifier of the image into Docker HUB (e.g., "sha256:5b117edd0b767986092e9f721ba2364951b0a271f53f1f41aff9dd1861c2d4fe")
      - *Architecture*: the architecture (e.g."amd64",)
      - *Os*: operating system of the image (e.g. "linux",)
      - *Size*: size of the image ibn bytes.
      - *RootFS*:
          *Layers*: list of the SHA256 of the layers  composing the image. 

  
### Examples
Retrive the JSON description of the image *ubuntu:12.04*
```
GET http://neri.di.unipi.it:3000/api/images?name=ubuntu:12.04
```
Result:
```
{
  "_id": "5a0f0867c90d2a001b0f07a2",
  "name": "ubuntu:12.04",
  "repo_name": "ubuntu",
  "stars": 6819,
  "pulls": 315987338,
  "description": null,
  "is_automated": false,
  "repo_owner": "",
  "tag": "12.04",
  "size": 39156124,
  "architecture": null,
  "repository": 130,
  "creator": 7,
  "last_updater": 2215,
  "last_updated": "2017-04-24T22:59:38.213Z",
  "image_id": null,
  "v2": true,
  "last_scan": "2017-11-17T16:03:50.457Z",
  "distro": "Ubuntu precise (12.04.5 LTS)",
  "status": "updated",
  "inspect_info": {
    "Id": "sha256:5b117edd0b767986092e9f721ba2364951b0a271f53f1f41aff9dd1861c2d4fe",
    "RepoTags": [
      "ubuntu:12.04"
    ],
    "RepoDigests": [
      "ubuntu@sha256:18305429afa14ea462f810146ba44d4363ae76e4c8dfc38288cf73aa07485005"
    ],
    "Parent": "",
    "Comment": "",
    "Created": "2017-04-12T21:05:30.976274223Z",
    "Container": "07f96280130f9446fcac0587da01f732228c62b460ab261fc4316f9ac32e6d76",
    "ContainerConfig": {
      "Hostname": "eb5b2868ea5d",
      "Domainname": "",
      "User": "",
      "AttachStdin": false,
      "AttachStdout": false,
      "AttachStderr": false,
      "Tty": false,
      "OpenStdin": false,
      "StdinOnce": false,
      "Env": [
        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
      ],
      "Cmd": [
        "/bin/sh",
        "-c",
        "#(nop) ",
        "CMD [\"/bin/bash\"]"
      ],
      "ArgsEscaped": true,
      "Image": "sha256:47e3f9ec5e6e59673b057bbbefad4aeccd33a53b98d1ff12ffa2f049b7981bba",
      "Volumes": null,
      "WorkingDir": "",
      "Entrypoint": null,
      "OnBuild": null
    },
    "DockerVersion": "1.12.6",
    "Author": "",
    "Config": {
      "Hostname": "eb5b2868ea5d",
      "Domainname": "",
      "User": "",
      "AttachStdin": false,
      "AttachStdout": false,
      "AttachStderr": false,
      "Tty": false,
      "OpenStdin": false,
      "StdinOnce": false,
      "Env": [
        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
      ],
      "Cmd": [
        "/bin/bash"
      ],
      "ArgsEscaped": true,
      "Image": "sha256:47e3f9ec5e6e59673b057bbbefad4aeccd33a53b98d1ff12ffa2f049b7981bba",
      "Volumes": null,
      "WorkingDir": "",
      "Entrypoint": null,
      "OnBuild": null
    },
    "Architecture": "amd64",
    "Os": "linux",
    "Size": 103592866,
    "VirtualSize": 103592866,
    "GraphDriver": {
      "Name": "aufs",
      "Data": null
    },
    "RootFS": {
      "Type": "layers",
      "Layers": [
        "sha256:58bcc73dcf4050a4955916a0dcb7e5f9c331bf547d31e22052f1b5fa16cf63f8",
        "sha256:9dc188d975fd7c511e3e40db68fcc5eb6290df063f36998c956fd147163fd821",
        "sha256:ee60293db08fc3111327cc7accc92798fd215ba7c148a6a7d6e1e3fd3b533efc",
        "sha256:73b4683e66e8ba13317b022e51f16960e0d436df40a772611e4d17248a721771",
        "sha256:3efd1f7c01f65eff325e5615c7b4913537017c633b0c83cba74f8ee1816df535"
      ]
    }
  },
  "__v": 0,
  "softwares": [
    {
      "software": "python",
      "ver": "2.7.3"
    },
    {
      "software": "perl",
      "ver": "5.14.2"
    },
    {
      "software": "erl",
      "ver": "2"
    },
    {
      "software": "bash",
      "ver": "4.2.25"
    },
    {
      "software": "tar",
      "ver": "1.26"
    }
  ]
		}
``` 

## Search API for searching images
The `/search` interface exposes the GET operation
that permits looking for (description of) images.

The query syntax is a list of *PAR* and *VALUE* pair separated by *&*.

```
GET /search?<PAR>=<VALUE>[&<PAR>=<VALUE>]*
```
The *PAR* can be:
- a software distribution to search in the image (e.g., *python*),
- any parameter namesdlisted in Table of the `GET /api/images`.

The *VALUE* depends on the PAR field.
- If the *PAR* is a software, the VALUE is the version of the software to search, (e.g. *python=2.7*)
- otherwise it is the value associated with the query parameters shown Table of the `GET /api/images`.


For example, if an user wants to retrieve all the images with *python 3.4*
and *bash 4.3* installed, the query submitted can be the following:

```
GET /search?python=3.4&bash=4.3
```

The response is a JSON of the form:
```
{
  "count": {Number},  // total number of documnets matching the query
  "page":{number},    // the page number submitted
  "limit":{Number},   // number of results per page submitted
  "pages":{pages},    // the total pages for retrieving all the results
  "images":           // list of images satisfying the query
    [
      {Image},
      {Image}
    ]  
}
```
### filter the results

| Example             | Description                                                                                       |
|-------------------------|---------------------------------------------------------------------------------------------------|
| GET /search?page=\<X\>    | Returns the page number X            |
| GET /search?limit=\<Y\>   | Limit as Y the number returned in a single page |
| GET /search?sort=\<pulls\> | -pulls | stars | -stars >   | Sorts the results by pull or stars |


User can filter the results of the previous query example by adding
additional parameters.


| Example                                       | Description                                                                                       |
|-----------------------------------------------|---------------------------------------------------------------------------------------------------|
| GET /search?python=3.4&bash=4.3&stars_gt=5    | Search images that have python3.4 ans bash 4.3 with a number of stars greater than 5.             |
| GET /search?python=3.4&bash=4.3&pulls_gte=5   | Search images that have python3.4 ans bash 4.3 with a number of pulls greater than or equal to 5. |
| GET /search?python=3.4&bash=4.3&size_lt=10000 | Search images that have python3.4 ans bash 4.3 with size less than 10000 bytes.                   |


# RESTful API of the images service
The API is exposed to the port `3000` on the endpoint `/api/images`

An image description is described by the *Mongoose Schema*:
```
{
  name: { // <repo:tag> the name id composed by: repository name : tag
      type:       String,
      unique:     true,
      required    :[true, 'The name of the image cannot be empty']
      },
  id_tag: Number,
  last_scan:      Date,
  last_updated:   Date,  // time of the last updated of the repo in the docker hub
  size:      Number,
  repository: Number,
  creator: Number,

  //Docker repository informations
  user:String,
  stars:     {
        type:       Number,
        min:        [0, 'stars must be positive number']
        },
  pulls:     Number,
  description:    String,
  is_automated: Boolean,
  is_private: Boolean,

    //Docker Finder informations
  distro: String,
  softwares: [{
          _id: false,
          software: String,
          ver: String
      }],

      status: String, // "pending" | "updated": if pending the image description must be updated.

      inspect_info:  mongoose.Schema.Types.Mixed  // docker run inpect <name>
```

### Retrieving images
The GET operation returns all the images stored into the local repository of Docker Finder.

```
GET /api/images
```

It returns a JSON, where *X*  is the number of total images returned, and *images* is an array of JSON object describiing the images.

```
{"count":<X>,
 "images":
    [
      {"_id":"58467ada8d8c26001116f167",
        "name":"onepill/docker-openresty:latest",
        "repository":1084992,
        "description":"OpenResty version of https://hub.docker.com/r/kyma/docker-nginx/",
        "status":"updated",
        "last_scan":"2016-12-06T08:46:18.414Z",
        "last_updated":"2016-12-01T16:15:08.892Z",
        "is_automated":null,
        "pulls":7,
        "creator":296143,
        "stars":0,
        "user":null,
        "distro":null,
        "id_tag":6517443,
        "is_private":null,
        "size":18645091,
        "softwares":[
              {"ver":"1.24.2","software":"httpd"},
              {"ver":"1.24.2","software":"wget"}
              ]
        "inspect_info":{ < contains all the information returned by docker inspect command >}
      },
    ...// the other images obejects
    ]
}
```

All the parameters of the `GET /api/images/` methods are shown in the table below:

| Parameter 	| Example                               	| description                                         	|
|-----------	|---------------------------------------	|-----------------------------------------------------	|
| sort      	| /api/images?sort=name                 	| Sorts the images by name in ascending order (A-Z).  	|
|           	| /api/images?sort=-name                	| Sorts the images by name in descending order (Z-A). 	|
| select    	| /api/images?select=*x*                	| Selects only the *x* attribute of the images.       	|
|           	| /api/images?select=name               	| Selects only the *name* of the images.                	|
| skip      	| /api/images?skip=5                    	| Skips the first 5 images.                           	|
| limit     	| /api/images?limit=5                   	| Returns the first 5 images.                         	|
| equals    	| /api/images?name__equals=nginx        	| Returns the image with name *nginx*.                  	|
|           	| /api/images?name=nginx                	| Returns the image with name *nginx*.                  	|
| ne        	| /api/images?name__ne=nginx            	| Returns  images who are not name *nginx*.             	|
| gt        	| /api/images?size__gt=200              	| Gets images with size > 200 bytes.                  	|
| gte       	| /api/images?size__gte=200             	| Gets images with size ≥ 200 bytes.                  	|
| lt        	| /api/images?size__lt=200              	| Gets images with size < 200 bytes.                  	|
| lte       	| /api/images?size__lte=200             	| Gets images with size ≤ 200 bytes.                  	|
| in        	| /api/images?size__in=30,200           	| Gets images with size 30 or 200 bytes               	|
| nin       	| /api/images?size__nin=18,30           	| Gets images with size not 18, 30.                   	|
| regex     	| /api/images?description__regex=Docker 	| Gets images with *Docker* in description.             	|



#### Adding new images
In order to add a new description of an image, the POST
method is used.
```
POST /api/images
```
The body of the request contains the JSON object of the image description
to add. An example of a request it is shown below.

```
POST / api / images
{
    "name":"onepill/docker-openresty:latest",
    "repository":1084992,
    "description":"OpenResty version of https://hub.docker.com/r/kyma/docker-nginx/",
    "status":"updated",
    "last_scan":"2016-12-06T08:46:18.414Z",
    "last_updated":"2016-12-01T16:15:08.892Z",
    "is_automated":null,
    "pulls":7,
    "creator":296143,
    "stars":0,
    "user":null,
    "distro":null,
    "id_tag":6517443,
    "is_private":null,
    "size":18645091,
    "softwares":[
        {"ver":"1.24.2","software":"httpd"},
        {"ver":"1.24.2","software":"wget"}
        ]
     "inspect_info":{ < contains all the information returned by docker inspect command >}

}
```
### Updating images
The PUT method permits updating the description of an image, whose the unique identifier is *id*.

```
PUT /api/images/:id
```
The body of the request contains the values of the image to update. In
the example below only the *name* and description fields of the
image with id 000011112222 are updated.
```
PUT / api / images /000011112222
{
  "name" : "repositoy/newname" ,
  "description" : "New description of the image"
}
```

### Deleting images
The HTTP method DELETE permits to delete an image
description. The *id* is the unique identifier of the image to delete.

```
DELETE /api/images/:id
```



