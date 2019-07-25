from google.appengine.ext import ndb
from Users import User
from Like import *

class Comment (ndb.Model):
    user = ndb.KeyProperty(User)
    user_name = ndb.StringProperty()
    content = ndb.StringProperty()
    likes = ndb.IntegerProperty(default = 0)
    likes_list = ndb.KeyProperty(Like,repeated=True)


