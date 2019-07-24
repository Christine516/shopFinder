from google.appengine.ext import ndb
from google.appengine.api import images

class Post (ndb.Model):
<<<<<<< HEAD
    image = ndb.BlobProperty()
=======
    image = ndb.BlobKeyProperty()
>>>>>>> 0dea26d116666321c02bc6855a2583a2f9ee8193
    image_url = ndb.StringProperty()
    tag1 = ndb.StringProperty()
    tag2 = ndb.StringProperty()
    tag3 = ndb.StringProperty()

    def create_post_photo_url(self):
        return images.get_serving_url(self.image)
