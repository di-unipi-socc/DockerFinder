# Server images Api documentation

An image is represented by the Schema.
```
{
    name:    String,  // <repo:tag>
 
    /// info of a particular tagged  image
    id_tag: Number,
    last_scan:      Date,    // Date of the last scan performaed by Docker finder
    last_updated:   Date,    // Date of the last:updated of the tag in the docker hub
    size:      Number,       
    repository: Number,       // Reference number of the repository
    creator: Number,

    //Docker repository information
    user:String,              // user of the repository
    stars:  Number            // The number of stars of the repository
    pulls:     Number,        // The number of pulls of the repository
    description:    String,   // Description of the repository
    is_automated: Boolean,    // if the repository is automated
    is_private: Boolean,       // if the repository is aprivate

    //Docker Finder information
    distro:     String,       // The operating system of the iamge
    softwares:       [{       // the list of the software versions found in the images
        software: String,
        ver: String
    }],

    inspect_info:  mongoose.Schema.Types.Mixed  //the result of  $docker inspect <image:tag>
}
```

## Search images

All the requests are in `GET` operation on the path `/search?`

In order to search the images with a software with version.  
`<software>=<version>`

Example: search all the images with java 1.8 and python 3.4

`GET /search?java=1.8&python=3.4`

### Sorting method
Is possible to require to return the images sorted by the stars or the pulls.

The parameter is  `sort=<star|pull>`

The reverse order is specified  by putting a `-` in front.

Example: search the images with python 2.7 ordering the result by the star 
from the image with less stars.

`GET /search?python=2.7&sort=-star`


