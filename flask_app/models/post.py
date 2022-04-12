


from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 

class Post:
    database = "pump_schema"
    def __init__(self,data):
        self.id = data['id']
        self.upload_photo = data['upload_photo']
        self.description = data['description']
        self.login_id = None
        # self.cheers = None
        
    @classmethod
    def allPostsWithUsers(cls):
        query = "SELECT posts.*, logins.username, logins.first_name, logins.last_name FROM posts JOIN logins on login_id = logins.id;"
        results = connectToMySQL(cls.database).query_db(query)
        posts = []
        for post in results:
            login_data = {
                'login_id' : post['login_id'],
                'username' : post['username'],
                'first_name' : post['first_name'],
                'last_name' : post['last_name']
            }
            post_data={
                'id' : post['id'],
                'upload_photo' : post['upload_photo'],
                'description' : post['description'],
                'login_id' : login_data
            }
            posts.append((post_data))
        print(posts)
        return posts 

    @classmethod
    def viewPosts(cls,data):
        query = "SELECT *  FROM posts where posts.id = %(id)s"
        results = connectToMySQL(cls.database).query_db(query,data)
        return cls(results[0])

    @classmethod
    def create_post(cls,data):
        query = "INSERT INTO posts (upload_photo,description,login_id) VALUES (%(upload_photo)s, %(description)s, %(login_id)s);"
        return connectToMySQL(cls.database).query_db(query,data)
    
    @classmethod
    def yourPosts(cls,data):
        query = "SELECT * FROM posts WHERE login_id = %(login_id)s;"
        results = connectToMySQL(cls.database).query_db(query,data)
        return results

    @classmethod
    def deletePost(cls,data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL(cls.database).query_db(query,data)
    
    @classmethod
    def likePost(cls,data):
        query = "INSERT INTO cheers (post_id,login_id) VALUES (%(post_id)s,%(login_id)s) ;"
        return connectToMySQL(cls.database).query_db(query,data)
    
    @classmethod
    def likeCount(cls,data):
        query = 'SELECT COUNT(id) FROM cheers where post_id = %(post_id)s ;'
        return connectToMySQL(cls.database).query_db(query,data)