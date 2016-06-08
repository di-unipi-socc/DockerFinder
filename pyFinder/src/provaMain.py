from pyDescriptor import DockerClient
from pyDescriptor import MongoClientPy


if __name__ == "__main__":

    d = DockerClient()
    m = MongoClientPy()
    info=d.extractInfo("mongo")
    m.insert_image(info)

