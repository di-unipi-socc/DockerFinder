from pyDescriptor import Scanner
from pyDescriptor import Crawler
from pyDescriptor import Client


if __name__ == "__main__":
    c = Crawler('doHub', host="172.17.0.2")
    #c.crawl()
    print(str([c.repo_name for c in c.get_crawled_images()]))

    #image = "nginx"
    #pull_image(image)

    s = Scanner()
    p = s.scan('python')
    # enricobomma/docker-whale
    #for im in c.get_crawled_images():
    #   image = s.scan(im.repo_name)


    c = Client('127.0.0.1',3000)
    print(c.post_image(p))




