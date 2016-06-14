from mongoengine import *
from .hub import Hub
from .bin import Bin

class Image(Document):

    repo_name_tag = StringField(required=True, primary_key=True) #name:tag
    t_scan = DateTimeField(null="None")
    #t_crawl = fields.DateTimeField(null="None")
    #layers = ListField(StringField(max_length=50))  #sha256 layers IDs
    size = StringField()
    hub = EmbeddedDocumentField(Hub)        # docker hub info
    bins = ListField(EmbeddedDocumentField(Bin))  # pyfinder results
    distro = StringField()

    def __str__(self):
        # Do whatever you want here
        return "Name : {0} \n Hub: {1} \n distro: {2} , \n bins: {3}".\
            format(self.repo_name_tag, self.hub, self.distro, '\n\t'.join(str(k) for k in self.bins))

