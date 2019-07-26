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
from all_posts import allPosts
from Login import *
from posts import *
from searchbytag import *
from Users import *
from Comment import *
from Like import *
from time import sleep
# the handler section
the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    @user_required
    def get(self):
        #
        if self.user.logged_in:

            query=Post.query().order(-Post.amount_comments)
            print(query)
            popular_posts=query.fetch(limit = 6)
            print(popular_posts)
            if len(popular_posts) > 5:
                query = Post.query(Post.user == self.user.key)
                all_user_posts = query.fetch()
                print(all_user_posts)
                params = {
                    "popularPost1": popular_posts[0],
                    "popularPost2": popular_posts[1],
                    "popularPost3": popular_posts[2],
                    "popularPost4": popular_posts[3],
                    "popularPost5": popular_posts[4],
                    "popularPost6": popular_posts[5],
                    "first_name": self.user.first_name,
                    "all_posts": all_user_posts,
                    "user": self.user,
                    "logged_in": True
                }
            else:
                query = Post.query(Post.user == self.user.key)
                all_user_posts = query.fetch()
                print(all_user_posts)
                params = {
                    "first_name": self.user.first_name,
                    "all_posts": all_user_posts,
                    "logged_in": True,
                    "user": self.user
                }
            upload_url = blobstore.create_upload_url('/')
        self.response.out.write(template.render("templates/home.html", params).format(upload_url))



    def post(self):
        # self.response.headers.add_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
        # self.response.headers.add_header("Expires","0")
        uploads = self.get_uploads()
        query = Post.query(Post.user == self.user.key)
        all_user_posts = query.fetch()
        query=Post.query().order(-Post.amount_comments)
        popular_posts=query.fetch(limit = 6)
        if uploads:
            upload = uploads[0]
            tags = [self.request.get("tag1"), self.request.get("tag2"), self.request.get("tag3")]

            post = Post(tags=tags,user=self.user.key,user_name = self.user.username)
            post.image = upload.key()
            post.image_url = images.get_serving_url(post.image)
            post.put()
            all_user_posts.append(post)
            if len(popular_posts) > 5:
                template_vars = {
                    "popularPost1": popular_posts[0],
                    "popularPost2": popular_posts[1],
                    "popularPost3": popular_posts[2],
                    "popularPost4": popular_posts[3],
                    "popularPost5": popular_posts[4],
                    "popularPost6": popular_posts[5],
                    "all_posts":all_user_posts,
                    "user": self.user
                }
            else:
                template_vars = {
                    "all_posts":all_user_posts,
                    "user": self.user
                }
        else:
            if len(popular_posts) > 5:
                template_vars = {
                    "popularPost1": popular_posts[0],
                    "popularPost2": popular_posts[1],
                    "popularPost3": popular_posts[2],
                    "popularPost4": popular_posts[3],
                    "popularPost5": popular_posts[4],
                    "popularPost6": popular_posts[5],
                    "all_posts":all_user_posts,
                    "user": self.user
                }
            else:
                template_vars = {
                    "all_posts":all_user_posts,
                    "user": self.user
                }
        upload_url = blobstore.create_upload_url('/')
        self.response.out.write(template.render("templates/home.html", template_vars).format(upload_url))
class LikePost(BaseHandler):
    @user_required
    def post(self):
        post_key = self.request.get("post")
        post = Post.get_by_id(int(post_key))
        like = Like(user_name = self.user.username)
        like.put()
        post.likes_list.append(like)
        post.likes += 1
        post.put()
        sleep(0.05)
        upload_url = blobstore.create_upload_url('/')
        query = Post.query(Post.user_name == self.user.username)
        all_posts = query.fetch()
        template_vars = {
            "all_posts": all_posts,
            "user": self.user
        }
        self.response.out.write(template.render("templates/home.html", template_vars).format(upload_url))




class CommentPostPage(BaseHandler):
    @user_required
    def post(self):
        comment_content = self.request.get("comment")
        print(comment_content)
        post_key = self.request.get("post")
        print(post_key)
        post = Post.get_by_id(int(post_key))
        comment = Comment(user=self.user.key, user_name=self.user.username,content=comment_content)
        comment.put()
        post.comments.append(comment.key)
        post.amount_comments = len(post.comments)
        post.put()
        sleep(0.05)
        upload_url = blobstore.create_upload_url('/')
        query = Post.query(Post.user_name == self.user.username)
        all_posts = query.fetch()
        template_vars = {
            "all_posts": all_posts,
            "user":self.user
        }
        print(self.response.out.write(template.render("templates/home.html", template_vars).format(upload_url)))

class CreateProfilePage(BaseHandler,blobstore_handlers.BlobstoreUploadHandler):
    @user_required
    def get(self):
        params = {
          'first_name': self.user.first_name,
        }
        upload_url = blobstore.create_upload_url('/Create')
        self.response.out.write(template.render("templates/CreateProfile.html", params).format(upload_url))

    def post(self):
        upload = self.get_uploads()[0]
        self.user.user_photo = upload.key()
        brand = self.request.get('Brand')
        gender = self.request.get('gender')
        self.user.brand = brand
        self.user.gender = gender
        self.user.put()
        self.render_template("home.html")

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
    webapp2.Route('/allPosts', handler=allPosts, name='all-Posts'),
    webapp2.Route('/search-results', handler=SearchResults, name='search-results'),
    webapp2.Route('/comment', handler=CommentPostPage, name='CommentPost'),
    webapp2.Route('/Like', handler=LikePost, name='LikePost'),
    webapp2.Route('/Create', handler=CreateProfilePage, name='CreateProfile'),
], debug=True,config=config)
