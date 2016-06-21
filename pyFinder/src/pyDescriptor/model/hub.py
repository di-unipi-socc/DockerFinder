from mongoengine import *

class Hub(Document):
    """
    Image description from Docker Hub.
    """
    repo_name = StringField(primary_key=True, required=True)
    pull_count = IntField()
    star_count = IntField()
    is_automated = BooleanField()
    is_official = BooleanField()
    repo_owner = StringField()
    short_description = StringField()

    t_crawl = DateTimeField(default=None)

    def __str__(self):
        return " \n\t repo_name: {0} \n\t pulls: {1} \n\t stars: {2} \n\t is_official {3} \n\t is_automated:{4} " \
               "\n\t repo_owner: {5}, \n\t short_description:{6} \n ".\
                format(self. repo_name,self.pull_count, self.star_count, self.is_official, self.is_automated,
                       self.repo_owner, self.short_description)
