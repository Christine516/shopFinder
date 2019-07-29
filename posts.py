from google.appengine.ext import ndb
from Users import User
from Comment import Comment
from Like import Like

class Post (ndb.Model):
    image_url = ndb.StringProperty()
    comments = ndb.KeyProperty(Comment,repeated=True)
    likes = ndb.IntegerProperty(default = 0)
    likes_list = ndb.StructuredProperty(Like,repeated=True)
    tags = ndb.StringProperty(repeated=True)
    user= ndb.KeyProperty(User,required=True)
    user_name = ndb.StringProperty(required=True)
    amount_comments = ndb.IntegerProperty(default=0)

    def users_liked(self):
        users = []
        for like in self.likes_list:
            users.append(like.user_name)
        return users

