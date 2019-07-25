from google.appengine.ext import ndb


class LikePost(ndb.Model):
    user_name = ndb.StringProperty()

class LikeComment (ndb.Model):
    user_name = ndb.StringProperty()
