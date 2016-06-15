from mongoengine import *

class Hub(EmbeddedDocument):
    """   "star_count": 0,
    "pull_count": 236,
    "repo_owner": null,
    "short_description": " ",
    "is_automated": true,
    "is_official": false,
    "repo_name": "jess/audacity"
    """
    pull = IntField()
    stars = IntField()
    is_automated = BooleanField()
    is_official = BooleanField()
    repo_owner = StringField()
    short_description = StringField()

    def __str__(self):
        # Do whatever you want here
        return "\n\t pulls: {0} \n\t is_official {1} \n\t is_automated:{2} " \
               "\n\t repo_owner: {3}, \n\t short_description:{4} \n ".\
                format(self.pull, self.is_official, self.is_automated, self.repo_owner, self.short_description)
