from google.appengine.ext import ndb

class Post (ndb.Model):
    image = ndb.ImageProperty()
    tag1 = ndb.StringProperty()
    tag2 = ndb.StringProperty()
    tag3 = ndb.StringProperty()
