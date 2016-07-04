from pyDescriptor import Scanner
from pyDescriptor import Crawler
from pyDescriptor import Uploader
import json


if __name__ == "__main__":


    c = Crawler()
    u = Uploader('127.0.0.1', 3000)
    s = Scanner()

    print(u.get_images())
    #c.crawl(page_size=10,tot_image=10)

    #print(len(c.get_crawled_images()))
    #print(str([c.repo_name for c in c.get_crawled_images()]))

    #image = "nginx"
    #pull_image(image)


    p = s.scan('editoo/utils')
    u.post_image(p)
    #print(p)
    #u = s.scan('ubuntu')

    #j = s.scan('nginx')
    #print(json.dumps(p, indent=4))
    # enricobomma/docker-whale

    #response = c.post_image(p)
   # print(response)
    # print(c.get_images())


    # for im in c.get_crawled_images():
    #      if im.repo_name !="luminarytech/recchanges-server-prod":
    #          image = s.scan(im.repo_name)
    #          print(im)
    #          u.post_image(image)






