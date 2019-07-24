import webapp2
import jinja2
import os
# from google.cloud import datastore
from webapp2_extras import auth
from webapp2_extras import sessions
from google.appengine.ext.webapp import template
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
from google.appengine.api import images
from all_users_Posts import *
from Login import *
from posts import *
# the handler section
the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    @user_required
    def get(self):
        if self.user.logged_in:
            params = {
              'first_name': self.user.first_name,
              'logged_in': True
            }
            upload_url = blobstore.create_upload_url('/')
        self.response.out.write(template.render("templates/home.html", params).format(upload_url))


    def post(self):
        upload = self.get_uploads()[0]
        tag1_inputted = self.request.get("tag1")
        tag2_inputted = self.request.get("tag2")
        tag3_inputted = self.request.get("tag3")

        post = Post(tag1 = tag1_inputted, tag2 = tag2_inputted, tag3 = tag3_inputted)
        post.image = upload.key()
        post.image_url = images.get_serving_url(post.image)

        query=Post.query()
        all_posts=query.fetch()
        all_posts.append(post)
        post.put()

        template_vars = {
        "all_posts":all_posts,
        }
        template = the_jinja_env.get_template('templates/home.html')
        self.response.write(template.render(template_vars))
# the app configuration section
config = {
  'webapp2_extras.auth': {
    'user_model': 'Users.User',
    'user_attributes': ['username','password','first_name','last_name']
  },
  'webapp2_extras.sessions': {
    'secret_key': '\x0cWh\xd4|\xfd\xe6G\xba\x06\xf7)\xcf\xd32\x14\xc4\xbe\x8e\x10=\x87-r'
  }
}
app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=MainPage, name='home'),
    webapp2.Route('/Logout', handler=LogOutPage, name='logout'),
    webapp2.Route('/Login', handler=LoginPage, name='login'),
    webapp2.Route('/sign_up', handler=SignUpPage, name='SignUp'),
    webapp2.Route('/allUserPosts', handler=allUserPosts, name='all posts'),
], debug=True,config=config)
