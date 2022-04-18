


from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 

class Post:
    database = "pump_schema" #cls.database name 
    def __init__(self,data): # __init__ for post class
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.login_id = None #login information per post if their is a joing table
        self.cheers_count = 0 # ammount of cheers per post if their is a joining table
        self.cheered_by_user = False # if the loged in user has liked the post or not
        
    
    @classmethod # this method is not being used 
    def allPostsWithUsers(cls): #method for recieving all posts with user information
        query = "SELECT posts.*, logins.username, logins.first_name, logins.last_name FROM posts JOIN logins on login_id = logins.id;"
        results = connectToMySQL(cls.database).query_db(query) # make the database results into a variable "results"
        posts = [] # empty array
        for post in results: #looping through results
            login_data = { #data dictionary for login data 
                'login_id' : post['login_id'],
                'username' : post['username'],
                'first_name' : post['first_name'],
                'last_name' : post['last_name']
            }
            post_data={ # data dictionary for post data 
                'id' : post['id'],
                'title' : post['title'],
                'description' : post['description'],
                'created_at' : post['created_at'],
                'login_id' : login_data # connecting login data into post data
            }
            posts.append((post_data))
        # print(posts)
        return posts 
    

    @classmethod 
    def allPostsWithUsersAndCheerCount(cls,data):# get all posts with user info and cheer information and orders by most recent
        query = """SELECT posts.*, logins.username, logins.first_name, logins.last_name, cheer_counts.* ,posts_cheered_by_user.* FROM posts 
        JOIN logins on login_id = logins.id 
        LEFT JOIN (SELECT post_id, COUNT(post_id) as cheer_count FROM cheers GROUP BY post_id) cheer_counts on posts.id = cheer_counts.post_id 
        LEFT JOIN (SELECT post_id as cheer_liked_by_login FROM cheers WHERE login_id = %(id)s) posts_cheered_by_user on posts.id = posts_cheered_by_user.cheer_liked_by_login
        ORDER BY posts.created_at DESC;""" 
        #
        results = connectToMySQL(cls.database).query_db(query,data) # make the database results into a variable "results"
        posts = [] # empty array
        for post in results: #looping through results
            this_post_instance = cls(post) # creating an instance of the post 
            cheer_data = { #creating a data dictionary that hold cheer table data
                'post_id': post['post_id'],
                'cheer_count': post['cheer_count'],
                'cheer_liked_by_login': post['cheer_liked_by_login']
            }
            login_data = { #data dictionary for login data 
                'login_id' : post['login_id'],
                'username' : post['username'],
                'first_name' : post['first_name'],
                'last_name' : post['last_name']
            }
            post_data={ # data dictionary for post data 
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
        # print("this is Posts Array:", posts)
        # print("this is results",results)
        return posts 


    @classmethod # this method is not being used 
    def viewPostsWithLogin(cls,data): #specific post with user information 
        query = "SELECT posts.*, logins.username, logins.first_name, logins.last_name FROM posts JOIN logins on logins.id = login_id where posts.id = %(id)s; "
        results = connectToMySQL(cls.database).query_db(query,data)
        return results[0]

    @classmethod
    def viewPostWithLoginWithCheers(cls,data): # specific post with user information and cheer information
        query = """SELECT posts.*, logins.username, logins.first_name, logins.last_name, cheer_counts.*, posts_cheered_by_user.* FROM posts
        JOIN logins on logins.id = login_id 
        LEFT JOIN (SELECT post_id, COUNT(post_id) as cheer_count FROM cheers GROUP BY post_id) cheer_counts on posts.id = cheer_counts.post_id 
        LEFT JOIN (SELECT post_id as cheer_liked_by_login FROM cheers WHERE login_id = %(id)s) posts_cheered_by_user on posts.id = posts_cheered_by_user.cheer_liked_by_login
        where posts.id = %(post_id)s;"""
        results = connectToMySQL(cls.database).query_db(query,data) # make the database results into a variable "results"
        this_post_instance = cls(results[0]) # creating an instance of the post 
        # print(results)
        # print(results[0])
        # print(results[0]['cheer_count'])
        cheer_data = { # data dictionary to hold cheer table data 
                'post_id': results[0]['post_id'],
                'cheer_count': results[0]['cheer_count'],
                'cheer_liked_by_login': results[0]['cheer_liked_by_login']
            }
        login_data = { #data dictionary to hold login information
                'login_id' : results[0]['login_id'],
                'username' : results[0]['username'],
                'first_name' : results[0]['first_name'],
                'last_name' : results[0]['last_name']
            }
        if cheer_data['cheer_count'] != None: #if the number if cheers is over 0 
            this_post_instance.cheers_count = cheer_data['cheer_count'] #make this class instance cheer counts = the ammount
        # determine whether login cheered post or not (id if True, None if False)
        if cheer_data['cheer_liked_by_login'] != None:
            this_post_instance.cheered_by_user = True
        # print(this_post_instance.cheers_count)
        this_post_instance.login_id = login_data # place login data in the instance login_id space 
        return this_post_instance

    @classmethod
    def create_post(cls,data): # creating a post with insert
        query = "INSERT INTO posts (title,description,login_id) VALUES (%(title)s, %(description)s, %(login_id)s);"
        return connectToMySQL(cls.database).query_db(query,data)
    
    @classmethod
    def yourPosts(cls,data): # viewing posts with login id 
        query = "SELECT * FROM posts WHERE login_id = %(login_id)s ORDER BY posts.created_at DESC;"
        results = connectToMySQL(cls.database).query_db(query,data)
        return results

    @classmethod
    def deletePost(cls,data): # deleteing posts 
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL(cls.database).query_db(query,data)
    
    @classmethod
    def likePost(cls,data): # cheering post with the post id and login id 
        query = "INSERT INTO cheers (post_id,login_id) VALUES (%(post_id)s,%(login_id)s) ;"
        return connectToMySQL(cls.database).query_db(query,data)
    
    @classmethod
    def unlikePost(cls,data): # unliking post with login id and post id 
        query = "DELETE FROM cheers WHERE login_id = %(login_id)s AND post_id = %(post_id)s ;"
        return connectToMySQL(cls.database).query_db(query,data)
    
    @classmethod
    def likeCount(cls,data): #find out how many likes a post has with the count mysql function
        query = 'SELECT COUNT(id) FROM cheers where post_id = %(post_id)s ;'
        return connectToMySQL(cls.database).query_db(query,data)