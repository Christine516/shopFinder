from google.appengine.ext import ndb
from google.appengine.api import images
from Users import User
from Comment import Comment
from Like import LikePost
class Post (ndb.Model):
    image = ndb.BlobKeyProperty()
    image_url = ndb.StringProperty()
    comments = ndb.KeyProperty(Comment,repeated=True)
    likes = ndb.IntegerProperty(default = 0)
    likes_list = ndb.StructuredProperty(LikePost,repeated=True)
    tags = ndb.StringProperty(repeated=True)
    user= ndb.KeyProperty(User,required=True)
    user_name=ndb.StringProperty(required=True)
    amount_comments = ndb.IntegerProperty(default=0)

    def create_post_photo_url(self):
        return images.get_serving_url(self.image)
    def users_liked(self):
        users = []
        for like in self.likes_list:
            users.append(like.user.get())
        return users
    # def get_comment_name(self):

