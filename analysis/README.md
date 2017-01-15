# Analysis
```
Analysis
|
|___DockerFile_scanner: defines the scanner image.
|___DockerFile_crawler: defines the crawler image.
|___DockerFile_checker: defindes the cheker image.
|
|____pyFinder:
     |  
     |____pyfinder: the python  module  that defined the code of the scanner, crawler, checker
     |    |____model:
     |    |    |___image.py: the definition of the field |of an image in Docker Finder
     |    |____resources:
     |    |    |___logging.info: confiuration file for the logging
     |    |____tests
     |    |____checker.py: python class of the checker
     |    |____scanner.py: python class of the scanner
     |    |____crawler.py: python class of the crawler
     |    |____ ... (all the other classes)
     |
     |
     |____entryChecker.py: the entrypoint of the checker
     |____entryCrawler.py: the entrypoint of the Crawler
     |____entryScanner.py: the entrypoint of the Scanner.
```



## Crawler
Crawler crawls the images'name from a Docker registry. The are two possibilities:
  1. Crawl all the images from a registry
  2. Select a random uniform number of images from the Docker registry.


**random sampling: Streaming model & know sequence length**
 - S={i1, ...., in} is a sequence flowing through a channel and the input size *n* is known and big.
 - *m*  is the number of sampled items *m<n*.
 - No preprocessing possible: every item is considered once, the dicision to take the item is immediately and irrevocably. It is possible that fture items may kick out that one from the sample one.

 ```
s = 0
for (j=1 ; j <= n; j++)
  p = Rand(0,1)
  if (p <= (m-s)/ n-j+1):
     select S[j];
     s++
 ```



<!--

problems:
  - n is the total number of images: we don't know exactly because we discard non-latest images
  - n can vary during the crawling (it is not fixed)

resolutions:
  - crawler does not filter the latest images, it takes all the images.
  - we fix the n by taking the nubmer of images present in a certain time.


### Streaming model & UNKNOW sequence length
  - S is the stream of elements flowing through a channel.
  - *n* is the size of the stream, it is inknown (or change ??)
  - NO preprocessing is not possibile.
  - every item is considered once: the dicision to take the item is immediately and irrevocably


**reservoir sampling**
 - R[1,m] is the reservoir array, Initialilly contains the first m elements of the stream

  ``` (Knuth 1997)
  initialize array R[1,m] = S[1,m]   //first m element of the stream
  for each next item S[j]:
      h = rand(1,j)
      if h <= m:
        set R[h] = S[j]
  return array R
  ```
problems
  - crawler sends R to the queue only at the and (not an image at the time) -->


## scanner


## checker
