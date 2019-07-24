from google.appengine.ext import ndb
from google.appengine.api import images

class Post (ndb.Model):
    image = ndb.BlobProperty()
    image_url = ndb.StringProperty()
    tag1 = ndb.StringProperty()
    tag2 = ndb.StringProperty()
    tag3 = ndb.StringProperty()

    def create_post_photo_url(self):
        return images.get_serving_url(self.image)
