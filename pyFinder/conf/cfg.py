import os

# this is the key of the dictionary for constructing the description of the images
# are missing all the others ...
ID = "_id"
TAGS = "RepoTags"


VERSION_CMD_PATH = ""
main_base = os.path.dirname(__file__)
print(main_base)
config_file = os.path.join([main_base, "conf", "myproject.conf"])