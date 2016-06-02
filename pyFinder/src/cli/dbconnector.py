from pyFinder.src.cli.descriptor import imageDescriptor
from pymongo import MongoClient
from pymongo.errors import *
from pyFinder.src.cli import cfg

#client = MongoClient('mongodb://localhost:27017/')
#MongoClient()
#db = client.dofinder
#images = db.images


class FinderMongoClient:

    def __init__(self, host='mongodb://localhost:27017/'):
        client= MongoClient(host)
        db = client.dofinder
        self.images = db.images

    def insert_image(self, dict_image_info):
        try:
            sha_image = self.images.insert_one(dict_image_info).inserted_id      # bypass_document_validation=False
            print("Inserted into database "+ dict_image_info[cfg.TAGS])
        except DuplicateKeyError:
            print("Error: duplicated image in the database")

    def get_image(self, sha_image):
        return self.images.find_one({cfg.ID: sha_image})

    def count_all_images(self):
        return self.images.count()



c = FinderMongoClient('mongodb://172.17.0.2:27017/')
dict = imageDescriptor("java")
c.insert_image(dict)