"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        """
            This is an example of loading a model.
            Every controller has access to the load_model method.

            self.load_model('WelcomeModel')
        """

    """ This is an example of a controller method that will load a view for the client """
    def index(self):
        """ 
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_all_users()
        """
        return self.load_view('index.html')

    def create(self):
        format_user = {
        "first_name" : request.form['first_name'], 
        "last_name" : request.form['last_name'], 
        "email" : request.form['email'], 
        "password" : request.form['password'],
        "pw_check" : request.form['pw_check']
        }
        user_info = self.models['User'].create_user(format_user)
        if user_info['status'] == True:
            self.models['User'].create_user(user_info)
            return redirect('/users/success')
        else:
            for message in user_info['errors']:
                flash(message, 'regis_errors')
            return redirect('/')

    def login(self):

        user_info = {
        'email': request.form['email'],
        'password' : request.form['password']
        }
        user = self.models['User'].validate_user(user_info)
        if user['status'] == True:
            session['id'] = user['id']