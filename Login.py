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

  def display_message(self, message):
    """Utility function to display a template with a simple message."""
    params = {
      'message': message
    }
    self.render_template('message.html', params)

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
        params = {
          'bad_login': 'Yes',
          'bad_response': error
        }
        self.render_template('Login.html', params)

    def get(self):
        self.render_template('Login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        remember_var =  self.request.get('remember')
        try:
          u = self.auth.get_user_by_password(username, password, remember=True)
          self.redirect(self.uri_for('home'))
        except (InvalidAuthIdError, InvalidPasswordError) as e:
          if "InvalidPasswordError" in str(type(e)):
            self.error_login("Wrong password")
          else:
            self.error_login("Wrong username")


class SignUpPage(BaseHandler):
    def get(self):
        self.render_template('Signup.html')

    def post(self):
        first_name_var = self.request.get('first_name')
        last_name_var = self.request.get('last_name')
        username_var = self.request.get('username')
        password_var = self.request.get('password')
        remember_var = self.request.get('remember')
        email_var = self.request.get('email')
        unique_properties = ['email','username','password']
        user_data = self.user_model.create_user(username_var,unique_properties,username=username_var,email=email_var,
                                                password_raw=password_var,logged_in=True,first_name = first_name_var,
                                                last_name=last_name_var
                                                )
        if not user_data[0]:
            error = {
                'bad_login' : 'Yes',
                'bad_response' : 'Duplicates for %s ' % (user_data[1])
            }
            return self.render_template('Signup.html',error)
        user = user_data[1]
        if remember_var == "on":
            print("Remember function says checkbox is on")
            self.auth.set_session(self.auth.store.user_to_dict(user), remember=True)
        else:
            print("Remember function says checkbox is off")
            self.auth.set_session(self.auth.store.user_to_dict(user), remember=False)
        self.redirect(self.uri_for('home'))
