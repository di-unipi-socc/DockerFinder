from pymongo import MongoClient
from pymongo.errors import *

from . import cfg


class MongoClientPy:

    def __init__(self, host='mongodb://localhost:27017/'):
        client= MongoClient(host)
        db = client.dofinder        # name of the database
        self.images = db.images     # name of the table

    def insert_image(self, dict_image_info):
        try:
            sha_image = self.images.insert_one(dict_image_info).inserted_id      # bypass_document_validation=False
            print("Inserted into database " + dict_image_info[cfg.TAGS])
        except DuplicateKeyError:
            print("Error: duplicated image in the database")

    def get_image(self, sha_image):
        return self.images.find_one({cfg.ID: sha_image})

    def count_all_images(self):
        return self.images.count()

