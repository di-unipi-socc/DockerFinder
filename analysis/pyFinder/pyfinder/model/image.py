import json

class Image:

    def __init__(self):


        # property of a tagged image
        self.name = None            # string  'repo_name:tag'
        self.repo_nmae = None       # String   repo_name
        self.tag = None             #String    tag
        self.id_tag = None          # number
        self.last_updated = None    # "2016-06-12T15:46:20.873610Z
        self.last_updater  = None   # number
        self.size    = None         # number
        self.repository  = None     # number
        self.creator    = None      # number

        #last scan of DockerFinder
        self.last_scan = None       # str(datetime.now())

        # property of the repository
        self.user = None            # String
        self.stars = None           # Number
        self.pulls = None           # Number
        self.description = None     # String
        self.is_automated = None    # Bool
        self.is_official = None     # BOol
        self.is_private = None      # Bool

        # info of docker finder
        self.distro = None
        self.softwares = None # list =[{"software": <name>, "ver":<version>},]

        self.status = None  #  "pending" | "updated"

        # info inspect
        self.inspect_info = None  #


    def set_updated(self):
        self.status  = "updated"

    def set_pending(self):
        self.status  = "pending"

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return json.dumps(self.__dict__)

        
    # if 'star_count' in json_image:
    #     image.stars = json_image["star_count"]
    #
    # if 'pull_count' in json_image:
    #     image.pulls = json_image["pull_count"]
    #
    # if 'description' in json_image:
    #     image.description = json_image["short_description"]    # String
    #
    # if "is_automated" in json_image:
    #
    #     image.is_automated = json_image["is_automated"]      # Bool
    #
    # if "is_official" in json_image:
    #     image.is_official  = json_image["is_official"]
