
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
# import re
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# The above is used when we do login registration, be sure to install flask-bcrypt: pipenv install flask-bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = "users_schema" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # What changes need to be made above for this project?
        #What needs to be added her for class association?



    # Create Users Models
    @classmethod
    def save_user(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email)
        VALUES ( %(first_name)s, %(last_name)s, %(email)s)
        ;
        """
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name: Come on mate, no one can have a 1 letter name!")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name: Come on mate, no one can have a 1 letter name!")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            is_valid = False
            if user['email'] == '':
                flash("Email address cannot be blank.")
            elif '@' not in user['email']:
                flash("Invalid email address. Missing '@' symbol.")
            elif '.' not in user['email']:
                flash("Invalid email address. Missing domain extension (ex .com)")
            else:
                flash("Invalid email address. Please enter a valid email.")
        # check if email is unique
        user_emails = User.get_all_user_emails()
        if user['email'].lower() in user_emails:
            is_valid = False
            flash("That email is already taken!")
        return is_valid




    # Read Users Models
    @classmethod
    def get_all_users(cls):
        query = """
        SELECT * FROM users;
        """
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        
        for user in results: 
            users.append(cls(user))
        return users
    
    @classmethod
    def get_all_user_emails(cls):
        query = """
        SELECT email FROM users;
        """
        results = connectToMySQL(cls.db).query_db(query)
        emails = []
        for email in results:
            emails.append(email['email'].lower())

        return emails
    
    @classmethod
    def get_one_user(cls, user_id):
        query = """
            SELECT * FROM users
            WHERE id = %(id)s
            ;
            """
        data = {'id': user_id}
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])


    # Update Users Models
    @classmethod
    def update_user(cls, data):
        query = """
        UPDATE users 
        SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)




    # Delete Users Models
    @classmethod
    def delete_user(cls, user_id):
        query = """
        DELETE FROM users
        WHERE id = %(id)s;
        """
        data = {'id' : user_id}
        return connectToMySQL(cls.db).query_db(query, data)
