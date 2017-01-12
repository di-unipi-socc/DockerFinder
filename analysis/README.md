# Analysis part


## Crawler
Crawler crawls the images'name from a Docker registry. The are two possibilities:
  1. Crawl all the images from a registry
  2. Select a radmon uniform number of images.

**random sampling**: Given a sequence of items  S={i1, ...., in} and a positive numbe `m>n`, the goal is to select a subset o m items from S *uniformly at random*.
 - uniform sample from the range [1,n]
 - sample of size *m*

### Streaming model & know sequence length
 - S is flowing through a channel and the input size *n* is known and big.
 - NO preprocessing is not possibile.
 - every item is considered once: the dicision to take the item is immediately and irrevocably
 - future items may kick out that one from the sample one

 ```
s = 0
for (j=1 ; j <= n; j++)
  p = Rand(0,1)
  if (p <= (m-s)/ n-j+1):
     select S[j];
     s++
 ```

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
  - crawler sends R to the queue only at the and (not an image at the time)



## LambdaExecutor
```
def handler_name(event, context):
    ...
    return some_value
```

Example of searching Softwares

```
def handler_softwares(event, context):

    name = event.get('name')        # dockerfinder:scanner
    regex = event.get('regex')      # []
    command = event.get("command")  # python --version
    tag = event.get("tag")          # python

    client_daemon =  docker.Client(base_url='unix://var/run/docker.sock')

    container_id = client_daemon.create_container(image=name,
                                                        entrypoint="ping 127.0.0.1"
                                                        )['Id']
    try:
      client_daemon.start(container_id)
      
      created_exec = client_daemon.exec_create(container_id, cmd=command)
      output = client_daemon.exec_start(created_exec['Id'])

      version = None
      p = re.compile(regex)
        match = p.search(output)
        if match:
            version = match.group(0)
            return version
        client_daemon.stop(container_id)
    except :
        client_daemon.remove_container(container_id,force=True, v=True)

    client_daemon.remove_container(container_id, force=True, v=True)
    return version
```
