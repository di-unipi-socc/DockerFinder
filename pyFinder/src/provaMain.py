from pyDescriptor import Scanner
from pyDescriptor import Crawler
from pyDescriptor import pull_image

from pyDescriptor.model import image

if __name__ == "__main__":
    #c = Crawler('dofinder', host="172.17.0.2")
    #c.crawl()
    image = "nginx"
    pull_image(image)
    Image = Scanner().scan(image)
    print(Image)


