from google.appengine.ext import ndb
from google.appengine.api import images
from Users import *

class Comment (ndb.Model):
    user = ndb.KeyProperty(User)
    user_name = ndb.StringProperty()
    content = ndb.StringProperty()
    likes = ndb.IntegerProperty(default = 0)
    # comments = ndb.StructuredProperty(Comment,repeated=True)
