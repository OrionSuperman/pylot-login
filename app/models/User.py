""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import re

class User(Model):
    def __init__(self):
        super(WelcomeModel, self).__init__()

    def create_user(self, user_info):

        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        if not user_info['first_name']:
            errors.append('First name cannot be blank')
        elif len(user_info['first_name']) < 2:
            errors.append('First name must be at least 2 characters long')

        if not user_info['last_name']:
            errors.append('Last name cannot be blank')
        elif len(user_info['last_name']) < 2:
            errors.append('Last name must be at least 2 characters long')

        if not user_info['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(user_info['email']):
            errors.append('Email format must be valid!')

        if not user_info['password']:
            errors.append('Password must not be blank')
        elif len(user_info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif user_info['password'] != user_info['pw_check']:
            errors.append('Passwords must match!')

        if errors:
            return {'status':False, 'errors':errors}
        else:
            pw_hash = self.bcrypt.generate_password_hash(user_info['password'])
            query = "INSERT INTO users (first_name, last_name, email, pass_hash, created_at, updated_at) VALUES (%s, %s, %s, NOW(), NOW())"
            info = [user_info['first_name'], user_info['last_name'], user_info['email'], pw_hash]
            self.db.query_db(query, user_info)
            id_query = "SELECT id FROM users WHERE email=%s"
            id_email = user_info['email']
            user=self.db.query_db(id_query, id_email)
            session['id'] = theid[0]['id']
            return {'status':True, 'user':user}

    def validate_user(self, user_info):
        query = "SELECT * FROM users WHERE email=%s"
        info = [user_info['email']]
        user = self.db.query_db(query, info)
        pass_hash = user[0]['pass_hash']
        password = user_info['password']
        if self.bcrypt.check_password_hash(pass_hash, password):
            status = True
            session['id'] = user[0]['id']

    """
    Below is an example of a model method that queries the database for all users in a fictitious application

    def get_all_users(self):
        print self.db.query_db("SELECT * FROM users")

    Every model has access to the "self.db.query_db" method which allows you to interact with the database
    """

    """
    If you have enabled the ORM you have access to typical ORM style methods.
    See the SQLAlchemy Documentation for more information on what types of commands you can run.
    """
