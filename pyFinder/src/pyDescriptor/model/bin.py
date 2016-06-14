from mongoengine import *


class Bin(EmbeddedDocument):
    """
    "Bins": [
           {"Bin": NAME_BINARY
            "Ver": VERSION},
    ]"""
    bin = StringField()
    ver = StringField()

    def __str__(self):
        return "bin: {0}, ver: {1}".format(self.bin, self.ver)
