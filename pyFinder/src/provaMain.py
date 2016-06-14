from pyDescriptor import Scanner

if __name__ == "__main__":

    #crawlerDocker.crawl_all_images();

    s = Scanner('dofinder', host="172.17.0.2")
    image = s.scan("python:latest")

