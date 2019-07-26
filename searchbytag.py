from Login import *
from posts import *
import webapp2
import jinja2
import os

the_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class SearchResults(BaseHandler):
    @user_required
    def post(self):
        results = []
        search_input=self.request.get("search")
        all_posts=Post.query().fetch()
        for post in all_posts:
            for tag in post.tags:
                if tag == search_input:
                    results.append(post)
                    break

        template_vars = {
        "results":results,
        "user": {"username": "xyz"}
        }

        template = the_jinja_env.get_template('templates/search-results.html')
        self.response.write(template.render(template_vars))
