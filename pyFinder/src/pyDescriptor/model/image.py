from mongoengine import *
import datetime

from .bin import Bin

class Image(Document):

    repo_name_tag = StringField(required=True, primary_key=True) #name:tag
    t_scan = DateTimeField(default=datetime.datetime.utcnow)  # scan time of the image

    #layers = ListField(StringField(max_length=50))  #sha256 layers IDs
    size = StringField()
    distro = StringField()
    bins = ListField(EmbeddedDocumentField(Bin))  # pyfinder results


    #hub = EmbeddedDocumentField(Hub)        # docker hub info
    ## info from docker hub

    def __str__(self):
        # Do whatever you want here
        return "Name : {0} \n , \n distro: {1} , \n bins: {2} \n t_scan: {3} ". \
            format(self.repo_name_tag, self.distro, '\n\t'.join(str(k) for k in self.bins),
                   str(self.t_scan))

