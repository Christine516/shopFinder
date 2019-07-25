from webapp2_extras import auth
from webapp2_extras import sessions
from google.appengine.ext.webapp import template
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
from google.appengine.api import images
import webapp2
import jinja2
import os

def user_required(handler):
  """
    Decorator that checks if there's a user associated with the current session.
    Will also fail if there's no session present.
  """
  def check_login(self, *args, **kwargs):
    auth = self.auth
    print("Reached check login")
    if not auth.get_user_by_session():
        print("Check login doesn't work")
        self.redirect(self.uri_for('login'), abort=True)
    else:
        print("Check login works")
        return handler(self, *args, **kwargs)

  return check_login

class BaseHandler(webapp2.RequestHandler):
  @webapp2.cached_property
  def auth(self):
    """Shortcut to access the auth instance as a property."""
    return auth.get_auth()

  @webapp2.cached_property
  def user_info(self):
    """Shortcut to access a subset of the user attributes that are stored
    in the session.

    The list of attributes to store in the session is specified in
      config['webapp2_extras.auth']['user_attributes'].
    :returns
      A dictionary with most user information
    """
    return self.auth.get_user_by_session()

  @webapp2.cached_property
  def user(self):
    """Shortcut to access the current logged in user.

    Unlike user_info, it fetches information from the persistence layer and
    returns an instance of the underlying model.

    :returns
      The instance of the user model associated to the logged in user.
    """
    u = self.user_info
    return self.user_model.get_by_id(u['user_id']) if u else None

  @webapp2.cached_property
  def user_model(self):
    """Returns the implementation of the user model.

    It is consistent with config['webapp2_extras.auth']['user_model'], if set.
    """
    return self.auth.store.user_model

  @webapp2.cached_property
  def session(self):
      """Shortcut to access the current session."""
      return self.session_store.get_session(backend="datastore")

  def render_template(self, view_filename, params={}):
    user = self.user_info
    params['user'] = user
    path = os.path.join(os.path.dirname(__file__), 'templates', view_filename)
    self.response.out.write(template.render(path, params))

  # this is needed for webapp2 sessions to work
  def dispatch(self):
      # Get a session store for this request.
      self.session_store = sessions.get_store(request=self.request)

      try:
          # Dispatch the request.
          webapp2.RequestHandler.dispatch(self)
      finally:
          # Save all sessions.
          self.session_store.save_sessions(self.response)
class LogOutPage(BaseHandler):
    @user_required
    def get(self): #for a get request
        self.user.logged_in = False
        self.auth.unset_session()
        self.redirect(self.uri_for('login'))

class LoginPage(BaseHandler):
    def error_login(self, error):
        self.render_template('login.html')

    def get(self):
        self.render_template('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        try:
          u = self.auth.get_user_by_password(username, password)
          self.redirect(self.uri_for('home'))
        except (InvalidAuthIdError, InvalidPasswordError) as e:
          self.render_template('login.html')


class SignUpPage(BaseHandler):
    def get(self):
        self.render_template('signup.html')

    def post(self):
        first_name_var = self.request.get('first_name')
        last_name_var = self.request.get('last_name')
        username_var = self.request.get('username')
        password_var = self.request.get('password')

        unique_properties = ['username','password']
        user_data = self.user_model.create_user(username_var,unique_properties,username=username_var,
                                                password_raw=password_var,logged_in=True,first_name = first_name_var,
                                                last_name=last_name_var
                                                )
        if not user_data[0]:
            return self.render_template('signup.html')
        user = user_data[1]
        self.auth.set_session(self.auth.store.user_to_dict(user), remember=False)
        self.redirect(self.uri_for('CreateProfile'))
