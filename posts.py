from google.appengine.ext import ndb
from google.appengine.api import images
from Users import User
from Comment import Comment
class Post (ndb.Model):
    image = ndb.BlobKeyProperty()
    image_url = ndb.StringProperty()
    comments = ndb.StructuredProperty(Comment,repeated=True)
    likes = ndb.IntegerProperty(default = 0)
    tags = ndb.StringProperty(repeated=True)
    user= ndb.KeyProperty(User,required=True)
    user_name=ndb.StringProperty(required=True)
    amount_comments = ndb.IntegerProperty(default=0)

    def create_post_photo_url(self):
        return images.get_serving_url(self.image)
