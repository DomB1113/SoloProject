from sqlite3 import connect
from flask_app.models.post import Post
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
        query = "INSERT INTO followings (login_id, following_id) VALUES (%(login_id)s, %(following_id)s) ;"
        return connectToMySQL(cls.database).query_db(query,data)
    
    @classmethod
    def allLoginsFollowings(cls,data):
        query = "SELECT logins.id as user_id, follow.username, followings.*, posts.* FROM logins JOIN followings on logins.id = login_id JOIN posts on following_id = posts.login_id JOIN logins as follow on posts.login_id = follow.id where logins.id = %(id)s;"
        results = connectToMySQL(cls.database).query_db(query,data)
        print(results)
        return results
    
    @classmethod
    def allLoginsFollowingWithCheerCount(cls,data):
        query = """SELECT logins.id as user_id,  followings.*, posts.*,follow.username, cheer_counts.*,posts_cheered_by_user.* FROM logins 
            JOIN followings on logins.id = login_id 
            JOIN posts on following_id = posts.login_id 
            LEFT JOIN (SELECT post_id, COUNT(post_id) as cheer_count FROM cheers GROUP BY post_id) cheer_counts
            on posts.id = cheer_counts.post_id
            LEFT JOIN (SELECT post_id as cheer_liked_by_login FROM cheers WHERE login_id = %(id)s) posts_cheered_by_user
            on posts.id = posts_cheered_by_user.cheer_liked_by_login
            JOIN logins as follow on posts.login_id = follow.id 
            where logins.id = %(id)s ORDER BY posts.created_at DESC;"""
            # order by
        results = connectToMySQL(cls.database).query_db(query,data)
        posts = []
        for post in results:
            cheer_data = {
                'post_id': post['post_id'],
                'cheer_count': post['cheer_count'],
                'cheer_liked_by_login': post['cheer_liked_by_login']
            }
            login_data = {
                'login_id' : post['login_id'],
                'username' : post['username'],
            }
            post_data={
                'id' : post['id'],
                'title' : post['title'],
                'description' : post['description'],
                'created_at' : post['created_at'],
                'login_id' : login_data
                
            }
            this_post_instance = Post(post_data)
            # push login data into class object
            this_post_instance.login_id = login_data
            # push cheer count into class object 
            if post['cheer_count'] != None:
                this_post_instance.cheers_count = post['cheer_count']
            # determine whether login cheered post or not (id if True, None if False)
            if post['cheer_liked_by_login'] != None:
                this_post_instance.cheered_by_user = True
            posts.append((this_post_instance))
        print("this is Posts Array:", posts)
        print("this is results",results)
        return posts 
    
    @classmethod
    def loginsFollowings(cls,data):
        query = """SELECT logins.id as user_id,  followings.*, follow.username FROM logins 
            JOIN followings on logins.id = login_id 
            JOIN logins as follow on followings.following_id = follow.id 
            where logins.id = %(id)s;"""
        results = connectToMySQL(cls.database).query_db(query,data)
        print(results)
        return results

    @classmethod
    def followsLogin(cls,data):
        query= """SELECT logins.id as user_id,  followings.*, follow.username FROM logins 
            JOIN followings on logins.id = login_id 
            JOIN logins as follow on followings.login_id = follow.id 
            where following_id = %(id)s;"""
        results = connectToMySQL(cls.database).query_db(query,data)
        print(results)
        return results

        
    @classmethod
    def unFollowUser(cls,data):
        query = "DELETE FROM followings WHERE id = %(followings_id)s; "
        return connectToMySQL(cls.database).query_db(query,data)
