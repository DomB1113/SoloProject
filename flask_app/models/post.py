


from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 

class Post:
    database = "pump_schema"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.login_id = None
        self.cheers_count = 0
        self.cheered_by_user = False
        
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
                'title' : post['title'],
                'description' : post['description'],
                'created_at' : post['created_at'],
                'login_id' : login_data
            }
            posts.append((post_data))
        print(posts)
        return posts 
    #  here
    @classmethod 
    def allPostsWithUsersAndCheerCount(cls,data):
        query = """SELECT posts.*, logins.username, logins.first_name, logins.last_name, cheer_counts.* ,posts_cheered_by_user.* FROM posts 
        JOIN logins on login_id = logins.id 
        LEFT JOIN (SELECT post_id, COUNT(post_id) as cheer_count FROM cheers GROUP BY post_id) cheer_counts on posts.id = cheer_counts.post_id 
        LEFT JOIN (SELECT post_id as cheer_liked_by_login FROM cheers WHERE login_id = %(id)s) posts_cheered_by_user on posts.id = posts_cheered_by_user.cheer_liked_by_login;"""
        results = connectToMySQL(cls.database).query_db(query,data)
        posts = []
        for post in results:
            this_post_instance = cls(post)
            cheer_data = {
                'post_id': post['post_id'],
                'cheer_count': post['cheer_count'],
                'cheer_liked_by_login': post['cheer_liked_by_login']
            }
            login_data = {
                'login_id' : post['login_id'],
                'username' : post['username'],
                'first_name' : post['first_name'],
                'last_name' : post['last_name']
            }
            post_data={
                'id' : post['id'],
                'title' : post['title'],
                'description' : post['description'],
                'created_at' : post['created_at'],
                'login_id' : login_data
                
            }
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
    def viewPostsWithLogin(cls,data):
        query = "SELECT posts.*, logins.username, logins.first_name, logins.last_name FROM posts JOIN logins on logins.id = login_id where posts.id = %(id)s; "
        results = connectToMySQL(cls.database).query_db(query,data)
        return results[0]

    # @classmethod
    # def viewPostWithLoginWithCheers(cls,data):
    #     query = """SELECT posts.*, logins.username, logins.first_name, logins.last_name, cheer_counts.*,posts_cheered_by_user.* FROM posts 
    #         JOIN logins on logins.id = login_id 
    #         LEFT JOIN (SELECT post_id, COUNT(post_id) as cheer_count FROM cheers GROUP BY post_id) cheer_counts
    #         on posts.id = cheer_counts.post_id
    #         LEFT JOIN (SELECT post_id as cheer_liked_by_login FROM cheers WHERE login_id = %(id)s) posts_cheered_by_user
    #         on posts.id = posts_cheered_by_user.cheer_liked_by_login
    #         where posts.id = %(post_id)s;"""
    #     results = connectToMySQL(cls.database).query_db(query,data)
    #     return results[0]

    @classmethod
    def create_post(cls,data):
        query = "INSERT INTO posts (title,description,login_id) VALUES (%(title)s, %(description)s, %(login_id)s);"
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