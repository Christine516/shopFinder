from google.appengine.ext import ndb
from google.appengine.api import images

class Post (ndb.Model):
    image = ndb.BlobKeyProperty()
    image_url = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True)

    def create_post_photo_url(self):
        return images.get_serving_url(self.image)
