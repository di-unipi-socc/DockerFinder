# Discovery

```
Disvovery
|
|___softwareService:
|   |
|   |___software-server
|   |   |
|   |   |___models
|   |   |    |___software.js : described the class object of a Software.
|   |   |  
|   |   |___routes
|   |   |    |___software.js: defines the APIn interface for the Software.
|   |   |
|   |   |___DockerFile: used to build the images_server Docker image.
|   |   |       
|   |   |___software.json: initial set of Software for populate the database.
|   |
|   |___SoftwareManager.py: script python for UPLOAD, PULL, or RM the software list.
|
|___webapp: contains the code of the GUI.
   |
   |___public
   |   |___app: angular2 application files
   |   |
   |   |___typings: folder for the compiler typescript
   |   |
   |   |___index.html : inital HTML page of the application
   |
   |___server.js : defined the search proxy to the images_server and serves the web application.
   |
   |___Dockerfile : defined how to build the webapp Docker image

```
### SoftwareService
The Software service  manages the list of software that must be searched into each image. This list is exploited by the scanners
during the scanning phase of an image.


Each Software is defined by the *Mongoose Schema**:
```
name: {
    type: String,       // python | perl | wget
    unique: true
},
cmd: String,            // --version
regex: String           //regular expression

```

## Retrieving the list of software distribution

The GET method is used
to retrieve all the software distributions

```
GET /api/software
```

It returns a JSON object with all the software
```
{"count":16,
  "software":[
    {"_id":"587bb200201d400011e4785d",
      "name":"python",
      "cmd":"--version",
      "regex":"[0-9]+[.][0-9]*[.0-9]*"
      },
    ... // the rest of the objects describing the softwar
    ]
  }
```

## Adding a new software distribution
The POST method is used to add a new software distribution to the database.

```
POST / api / software
```

The body of the request contains the JSON object.

```
{
  "name" : "java" ,
  "cmd" : "-version" ,
  "regex" : "[0-9]*[.][0-9]*[a-zA-Z0-9_.-]*"
}

```

The response returns the unique identifier (*_id*) of the software added
into the database.

```

{
  "_id": "57 b16eb21d3ee62000fcc74b",
  "name" : "java" ,
  "cmd" : "-version" ,
  "regex" : "[0-9]*[.][0-9]*[a-zA-Z0-9_.-]*"
}
```

### Deleting a software distribution
The method DELETE is used to remove a
software distribution from the database. The id is the unique identifier
of the software to be deleted:

```
DELETE /api/software/:id
```

For deleting the software *java*  (of the previous example)
```
DELETE /api/images/57b16eb21d3ee62000fcc74b
```
## Updating a software distribution
The method PUT is used to update an existing software identified by id.

```
PUT /api/software/:id
```
The body of the request is a JSON with the fields value to update. In
the example below the software java is updatde with the *-v* command.

```
PUT /api/images/57b16eb21d3ee62000fcc74b
{
  "name" : "javaNew" ,
  "cmd" : "-v" ,
}
```

## GUI web application

<div  align="center">
<img src="../docs/df_gif.gif" width="500">
</div>
