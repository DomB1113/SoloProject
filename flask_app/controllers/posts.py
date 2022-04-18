
from flask_app.models.post import Post #importing Posts class 
from flask_app.models.login import Login #importing Login class
from flask_app import app # importing app from __init__.py 
# importing redirect to change routes during posts, requests for form data in mysql query, session to hold login information,
#rendertemplate to attach html to route, and flash for validation messages.
from flask import redirect, request, session, render_template, flash

@app.route('/likepost', methods = ['POST']) #route for cheering post on the homepage 
def likePost():
    if 'login_id' not in session: #checks if the login id is in sessions
        return redirect('/logout')
    data = { #data dictionary of which post is cheered and by which user
        'post_id':request.form['post_id'], 
        'login_id':request.form['login_id']
    }
    Post.likePost(data) 
    return redirect('/homepage')

@app.route('/unlikepost', methods = ['POST']) # route for uncheering post on the homepage
def unlikePost():
    if 'login_id' not in session: #checks if the login id is in sessions
        return redirect('/logout')
    data = { #data dictionary of which post is uncheered and by which user
        'post_id':request.form['post_id'],
        'login_id':request.form['login_id']
    }
    Post.unlikePost(data)
    return redirect('/homepage')

@app.route('/likepost/following', methods = ['POST']) #route for cheering post on the following
def likePostfollowing():
    if 'login_id' not in session:  #checks if the login id is in sessions
        return redirect('/logout')
    data = { #data dictionary of which post is cheered and by which user
        'post_id':request.form['post_id'],
        'login_id':request.form['login_id']
    }
    Post.likePost(data)
    return redirect('/following')

@app.route('/unlikepost/following', methods = ['POST']) #route for uncheering post on the following
def unlikePostfollowing():
    if 'login_id' not in session: #checks if the login id is in sessions
        return redirect('/logout')
    data = { #data dictionary of which post is uncheered and by which user
        'post_id':request.form['post_id'],
        'login_id':request.form['login_id']
    }
    Post.unlikePost(data)
    return redirect('/following')

@app.route('/view/post/<int:id>') # route for viewing specific post 
def viewPost(id):
    if 'login_id' not in session:#checks if the login id is in sessions
        return redirect('/logout')
    login_data={ #data dictionary for login id
        'id':session['login_id']
    }
    login = Login.get_by_id(login_data)  # get login info by login id
    data={ #data dictionary to view post by which loged in user 
        'id':session['login_id'],
        'post_id': id
    }
    post = Post.viewPostWithLoginWithCheers(data) #view post info with cheer data and if login cheered post 
    return render_template('view_post.html', post = post, login=login)

@app.route('/likepost/viewing', methods = ['POST']) #route to cheer viewed post 
def likeViewedPost():
    if 'login_id' not in session: #checks if the login id is in sessions
        return redirect('/logout')
    data = { # data dictionary to cheer post 
        'post_id':request.form['post_id'],
        'login_id':request.form['login_id']
    }
    Post.likePost(data)
    return redirect(f"/view/post/{request.form['post_id']}") # f string to return to viewed post screen 

@app.route('/unlikepost/viewing', methods = ['POST']) # route to unlike post 
def unlikeViewedPost():
    if 'login_id' not in session:
        return redirect('/logout')
    data = {
        'post_id':request.form['post_id'],
        'login_id':request.form['login_id']
    }
    Post.unlikePost(data)
    return redirect(f"/view/post/{request.form['post_id']}") # f string to return to viewed post screen 

@app.route('/follow/user', methods = ["POST"]) # route to follow user from viewing the post
def follow_user():
    data ={ #data dictionary to know which user is following which user 
        'login_id': request.form['login_id'],
        'following_id': request.form['following_id']
    }
    Login.FollowUser(data) # follow user class method
    return redirect('/homepage')

@app.route('/unfollow', methods = ["POST"]) # route to unfollow user in following html
def unfollow_user():
    data ={ # data dictionary for which login to remover from table
        'followings_id': request.form['following_id'],
        'login_id': request.form['login_id']
    }
    Login.unFollowUser(data) # unfollow class method 
    return redirect('/following')

@app.route('/post') #creat post route 
def post():
    if 'login_id' not in session:
        return redirect('/logout')
    data={
        'id':session['login_id']
    }
    login = Login.get_by_id(data) # get login by id 
    return render_template('create_post.html', login = login)

@app.route('/create/post', methods=['POST']) # create post route 
def createPost():
    if 'login_id' not in session: # check if login id is in sessions
        return redirect('/logout')
    print(request.form)
    data = { # data dictionary of post form 
        'title' : request.form['title'],
        'description' : request.form['description'],
        'login_id': session['login_id']
    }
    Post.create_post(data) # class method to create form
    return redirect('/your/posts') # redirect to all posts logins created 

@app.route('/your/posts') # your posts route to view logins created posts 
def yourPosts():
    if 'login_id' not in session:
        return redirect('/logout')
    data={#data dictionary for login info 
        'id':session['login_id']
    }
    login_data = { # data dictionary for finding posts 
        'login_id': session['login_id']
    }
    login = Login.get_by_id(data) # classmethod for login info 
    posts = Post.yourPosts(login_data) #classmethod for posts logins created
    return render_template('your_posts.html', login = login, posts = posts)

@app.route('/delete/post/<int:id>') # route to delete posts 
def deletePost(id):
    data= {# data dictionary passing in parameter of which post is being choosen
        'id':id
    }
    Post.deletePost(data) # delete post method
    return redirect('/your/posts') #REURN TO POSTS CREATED BY LOGIN