
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 

class Post:
    database = "pump_schema"
    def __init__(self,data):
        self.id = data['id']
        self.upload_photo = data['upload_photo']
        self.description = data['description']
        self.login_id = None
    
        