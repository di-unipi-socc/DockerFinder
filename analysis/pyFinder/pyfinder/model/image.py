import json


class Image:

    def __init__(self, from_dict_image):
        assert "name" in from_dict_image, "name (repo_name:tag) cannot be empty"
        # info Docker Hub

        # string  'repo_name:tag'
        self.name = from_dict_image["name"]

        # repository INFO
        self.repo_name = from_dict_image["repo_name"] if "repo_name" in from_dict_image else None
        self.stars = from_dict_image["star_count"] if 'star_count' in from_dict_image else None
        self.pulls = from_dict_image["pull_count"] if 'pull_count' in from_dict_image else None
        self.description = from_dict_image["short_description"] if 'description' in from_dict_image else None
        self.is_automated = from_dict_image["is_automated"]if "is_automated" in from_dict_image else None
        self.is_official = from_dict_image["is_official"] if "is_official" in from_dict_image else None
        self.repo_owner = from_dict_image["repo_owner"] if "repo_owner" in from_dict_image else None

        # tag INFO
        self.tag = from_dict_image["tag"] if "tag" in from_dict_image else None
        self.size = from_dict_image["full_size"] if "full_size" in from_dict_image else None
        self.architecture = from_dict_image["architecture"] if "architecture" in from_dict_image else None        # number
        #self.variant = from_dict_image["variant"] if "variant" in from_dict_image else None
        self.repository = from_dict_image["repository"] if "repository" in from_dict_image else None
        self.creator = from_dict_image["creator"] if "creator" in from_dict_image else None
        self.last_updater = from_dict_image["last_updater"] if "last_updater" in from_dict_image else None   # number
        self.last_updated = from_dict_image["last_updated"] if "last_updated" in from_dict_image else None    # "2016-06-12T15:46:20.873610Z
        self.repository = from_dict_image ["repository"] if "repository" in from_dict_image else None
        self.image_id = from_dict_image["image_id"] if "image_id" in from_dict_image else None
        self.creator = from_dict_image["creator"] if "creator" in from_dict_image else None      # number
        self.v2 = from_dict_image["v2"] if "v2" in from_dict_image else None

        # image info when it is pulled
        self.id = None

        # last scan of DockerFinder
        self.last_scan = None       # str(datetime.now())

        # info of DockerFinder
        self.distro = None
        self.softwares = None     # list =[{"software": <name>, "ver":<version>},]
        self.status = None          # "pending" | "updated"

        # docker inspect info
        self.inspect_info = None  #

    def set_updated(self):
        self.status = "updated"

    def set_pending(self):
        self.status = "pending"

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return json.dumps(self.__dict__)
