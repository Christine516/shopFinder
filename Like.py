from google.appengine.ext import ndb


class Like (ndb.Model):
    user_name = ndb.StringProperty()
    likedpost = ndb.KeyProperty()


