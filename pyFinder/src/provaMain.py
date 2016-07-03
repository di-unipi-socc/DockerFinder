from pyDescriptor import Scanner
from pyDescriptor import Crawler
from pyDescriptor import Client
import json


if __name__ == "__main__":


    c = Crawler('doHub', host="172.17.0.2")
    #c.crawl(page_size=10,tot_image=10)

    #print(len(c.get_crawled_images()))
    #print(str([c.repo_name for c in c.get_crawled_images()]))

    #image = "nginx"
    #pull_image(image)

    s = Scanner()
    p = s.scan('python')
    #u = s.scan('ubuntu')

    #j = s.scan('nginx')
    #print(json.dumps(p, indent=4))
    # enricobomma/docker-whale

    #response = c.post_image(p)
   # print(response)
    # print(c.get_images())

    client = Client('127.0.0.1', 3000)
    #for im in c.get_crawled_images():
    #  image = s.scan(im.repo_name)
    #  client.post_image(image)
    client.post_image(p)





