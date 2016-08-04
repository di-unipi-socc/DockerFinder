# Server images Api documentation


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


