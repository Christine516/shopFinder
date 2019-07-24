from google.appengine.ext import ndb
from google.appengine.api import images
from Users import User
from Comment import Comment
class Post (ndb.Model):
    image = ndb.BlobKeyProperty()
    user =  ndb.KeyProperty(User)
    user_name = ndb.StringProperty()
    image_url = ndb.StringProperty()
    tag1 = ndb.StringProperty()
    tag2 = ndb.StringProperty()
    tag3 = ndb.StringProperty()
    comments = ndb.StructuredProperty(Comment,repeated=True)
    likes = ndb.IntegerProperty(default = 0)

    def create_post_photo_url(self):
        return images.get_serving_url(self.image)

