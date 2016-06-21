from pyDescriptor import Scanner
from pyDescriptor import Crawler



if __name__ == "__main__":
    c = Crawler('doHub', host="172.17.0.2")
    #c.crawl()
    #print(str([c.repo_name for c in c.get_crawled_images()]))

    #image = "nginx"
    #pull_image(image)

    s = Scanner()
    # enricobomma/docker-whale
    for im in c.get_crawled_images():
        s.scan(im.repo_name)





