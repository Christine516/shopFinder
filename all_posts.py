import webapp2
import jinja2
import os

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

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class allPosts(BaseHandler):
    def get(self):
        query=Post.query()
        all_posts=query.fetch()
        template_vars = {
        "all_posts":all_posts,
        }
        template = the_jinja_env.get_template('templates/all_posts.html')
        self.response.write(template.render(template_vars))
