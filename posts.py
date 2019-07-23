from google.appengine.ext import ndb

class Post (ndb.Model):
    image = ndb.BlobKeyProperty()
    image_url = ndb.StringProperty()
    tag1 = ndb.StringProperty()
    tag2 = ndb.StringProperty()
    tag3 = ndb.StringProperty()
