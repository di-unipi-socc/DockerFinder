from pyDescriptor import DockerClient
from pyDescriptor import MongoClientPy
from pyDescriptor import crawlerDocker

if __name__ == "__main__":

    crawlerDocker.crawl_all_images();

    d = DockerClient()
    m = MongoClientPy(host="mongodb://172.17.0.2:27017/")
    info = d.extractInfo("java")
    m.insert_image(info)

