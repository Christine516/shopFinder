import time
import webapp2_extras.appengine.auth.models
from google.appengine.ext import ndb

from webapp2_extras import security
from google.appengine.api import images
from google.appengine.ext import ndb
from google.appengine.api import images
import webapp2


class User(webapp2_extras.appengine.auth.models.User):
    username = ndb.StringProperty(required=True)
    logged_in = ndb.BooleanProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    brand = ndb.StringProperty()
    gender = ndb.StringProperty()
    user_photo = ndb.BlobKeyProperty()
    # posts = ndb.KeyProperty(Post,repeated=True)

    def create_user_photo_url(self):
        return images.get_serving_url(self.user_photo) + "=s32"

    def set_password(self, raw_password):
        self.password = security.generate_password_hash(raw_password, length=12)
        return self.password

    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):

        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        # Use get_multi() to save a RPC call.
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp

        return None, None
