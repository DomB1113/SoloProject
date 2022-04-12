from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Login:
    database = "pump_schema"
    def __init__(self,data):
        self.id = data['id']
        self.username = data['username']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.birthday = data['birthday']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod 
    def insert(cls,data):
        query = "INSERT INTO logins (username,first_name,last_name,email,birthday,password) VALUES (%(username)s, %(first_name)s , %(last_name)s , %(email)s, %(birthday)s , %(password)s) ;"
        return connectToMySQL(cls.database).query_db(query,data)

    @staticmethod
    def validate_registration(data):
        is_valid = True 
        query = "SELECT * FROM  logins WHERE email = %(email)s ;"
        results = connectToMySQL('pump_schema').query_db(query,data)
        if len(results)>= 1:
            flash("Email is already taken", 'register')
            is_valid = False
        if len(data['username'])< 3:
            flash('Username must be at least 3 letters', 'register')
            is_valid = False
        if len(data['first_name'])< 3:
            flash('First Name must be at least 3 letters', 'register')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Last Name must be at least 3 letters', 'register')
            is_valid = False
        if len(data['email']) < 6:
            flash('email must be at least 6 letters', 'register')
            is_valid = False
        if len(data['birthday']) <7:
            flash('birthday needs to be filled out', 'register')
            is_valid = False
        if len(data['password']) < 6:
            flash('password needs to be 6 letters or more', 'register')
            is_valid = False 
        if data['password'] != data['confirm_password']:
            flash('Password dont match', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address')
            is_valid = False 
        return is_valid

    @staticmethod
    def validate_update(data):
        is_valid = True 
        if len(data['username'])< 3:
            flash('Username must be at least 3 letters', 'update')
            is_valid = False
        if len(data['first_name'])< 3:
            flash('First Name must be at least 3 letters', 'update')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Last Name must be at least 3 letters', 'update')
            is_valid = False
        if len(data['email']) < 6:
            flash('email must be at least 6 letters', 'update')
            is_valid = False
        if len(data['birthday']) <7:
            flash('birthday needs to be filled out', 'update')
            is_valid = False
        if len(data['password']) < 6:
            flash('password needs to be 6 letters or more', 'update')
            is_valid = False 
        if data['password'] != data['confirm_password']:
            flash('Password dont match', 'update')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid email address')
            is_valid = False 
        return is_valid

    @classmethod
    def update(cls,data):
        query = "UPDATE logins SET username = %(username)s, first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s , birthday = %(birthday)s , password = %(password)s  WHERE id = %(id)s "
        return connectToMySQL(cls.database).query_db(query,data)
    

    @classmethod 
    def get_by_email(cls,data):
        query = "SELECT * FROM logins WHERE email = %(email)s ;"
        results = connectToMySQL(cls.database).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod 
    def get_by_id(cls,data):
        query = "SELECT * FROM logins WHERE id = %(id)s ;"
        result = connectToMySQL(cls.database).query_db(query,data)
        return cls(result[0])


    @classmethod
    def FollowUser(cls,data):
        query = "INSERT INTO followings (login_id, follower_id) VALUES (%(login_id)s, %(follower_id)s) ;"
        return connectToMySQL(cls.database).query_db(query,data)
    
    @classmethod
    def allLoginsFollowings(cls,data):
        query = "SELECT logins.id as user_id, follow.username, followings.*, posts.* FROM logins JOIN followings on logins.id = login_id JOIN posts on follower_id = posts.login_id JOIN logins as follow on posts.login_id = follow.id where logins.id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query,data)
        return results
