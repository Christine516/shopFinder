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
from Login import *
from posts import *
from Comment import *
# the handler section
the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    @user_required
    def get(self):
        self.response.headers.add_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
        self.response.headers.add_header("Expires","0")
        if self.user.logged_in:
            params = {
              'first_name': self.user.first_name,
              'logged_in': True
            }
            upload_url = blobstore.create_upload_url('/')
        self.response.out.write(template.render("templates/home.html", params).format(upload_url))


    def post(self):
        self.response.headers.add_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
        self.response.headers.add_header("Expires","0")
        upload = self.get_uploads()[0]
        tag1_inputted = self.request.get("tag1")
        tag2_inputted = self.request.get("tag2")
        tag3_inputted = self.request.get("tag3")

        post = Post(tag1 = tag1_inputted, tag2 = tag2_inputted, tag3 = tag3_inputted,user = self.user.key,user_name = self.user.username)
        post.image = upload.key()
        post.image_url = images.get_serving_url(post.image)

        query = Post.query(Post.user_name == self.user.username)
        all_posts=query.fetch()
        all_posts.append(post)
        post.put()

        template_vars = {
            "all_posts":all_posts,
        }
        upload_url = blobstore.create_upload_url('/')
        self.response.out.write(template.render("templates/home.html", template_vars).format(upload_url))
class LikePost(BaseHandler):
    @user_required
    def post(self):
        post_key = self.request.get("post")
        post = Post.get_by_id(int(post_key))
        post.likes +=1
        post.put()

class CommentPostPage(BaseHandler):
    @user_required
    def post(self):
        comment_content = self.request.get("comment")
        print(comment_content)
        post_key = self.request.get("post")
        print(post_key)
        post = Post.get_by_id(int(post_key))
        comment = Comment(user=self.user.key, user_name =self.user.username,content=comment_content)
        comment.put()
        post.comments.append(comment)
        post.put()
        upload_url = blobstore.create_upload_url('/')
        query = Post.query(Post.user_name == self.user.username)
        all_posts = query.fetch()
        template_vars = {
            "all_posts": all_posts,
        }
        self.response.out.write(template.render("templates/home.html", template_vars).format(upload_url))





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
    webapp2.Route('/comment', handler=CommentPostPage, name='CommentPost'),
    webapp2.Route('/Like', handler=LikePost, name='LikePost'),
], debug=True,config=config)
