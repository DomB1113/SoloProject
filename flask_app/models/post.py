


from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 

class Post:
    database = "pump_schema"
    def __init__(self,data):
        self.id = data['id']
        self.upload_photo = data['upload_photo']
        self.description = data['description']
        self.login_id = None
    
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