import json

class Image:

    def __init__(self):

        # <repo_name:tag>
        # property of a tagged image
        self.name = None        # string
        self.id_tag = None    # number
        self.last_updated = None    # "2016-06-12T15:46:20.873610Z"
        self.last_scan = None       # str(datetime.now())
        self.last_updater  = None   # number
        self.size    = None        # number
        self.repository  = None    # number
        self.creator    = None    # number

        # property of the repository
        self.user = None
        self.stars = None
        self.pulls = None
        self.description = None
        self.is_automated = None
        self.is_private = None

        # info of docker finder
        self.distro = None
        self.softwares = None # list =[{"software": <name>, "ver":<version>},]

        # info inspect
        self.inspect_info = None  #

    def __repr__(self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return json.dumps(self.__dict__)
