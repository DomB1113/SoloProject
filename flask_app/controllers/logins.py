
from flask_app.models.post import Post #importing Posts class 
from flask_app.models.login import Login #importing Login class 
from flask_app import app # importing app from __init__.py 
# importing redirect to change routes during posts, requests for form data in mysql query, session to hold login information,
#rendertemplate to attach html to route, and flash for validation messages.
from flask import redirect, request, session, render_template, flash 
from flask_bcrypt import Bcrypt  #importing Bcrypt for password hashing (install flash-bcrypt in command)  
bcrypt = Bcrypt(app) # we are creating an object called bcrypt, 
                        # which is made by invoking the function Bcrypt with our app as an argument

@app.route('/login') #login page 
def loginpage():
    return render_template('login.html')

@app.route('/signup') #sign up page 
def signup():
    return render_template('signup.html')

@app.route('/register', methods = ['POST']) #registration post route
def register():
    if not Login.validate_registration(request.form): #if validation returns false
        return redirect('/signup')
    password_hash = bcrypt.generate_password_hash(request.form['password']) #hash password submitted
    print(password_hash)
    data ={ #data dictionary to hold form data 
        'username': request.form['username'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'birthday': request.form['birthday'],
        'password': password_hash # hashed password in mysql database for security 
    }
    
    login_id =Login.insert(data) #insert data into mysql database
    session['login_id'] = login_id #put login id into session
    return redirect('/homepage')

@app.route('/login', methods =['POST']) #login post route
def login():
    data = {
        'email': request.form['email'] #grab email in data dictionary
    }
    login_data = Login.get_by_email(data) #get login information by email
    if not login_data: #if the MySQL query returns false -> flash message
        flash('Invalid Email Address or Password', 'login')
        return redirect('/login')
    if not bcrypt.check_password_hash(login_data.password, request.form['password']): #if the hashed password does not match the hashed password submitted
        flash('Invalid Email Address or Password', 'login')
        return redirect('/login')
    session['login_id'] = login_data.id #place login id into sessions
    return redirect('/homepage')

@app.route('/homepage') # homepage route 
def homepage():
    if 'login_id' not in session: #checks if the login id is in sessions
        return redirect('/logout') #logs out user if not 
    data={
        'id':session['login_id']
    }
    login = Login.get_by_id(data)  #grabs login information using login id from sessions
    posts = Post.allPostsWithUsersAndCheerCount(data) #grabs all posts with their user information and their cheer information
    return render_template('homepage.html' , login = login , posts=posts) #connects html and brings in variables into html

@app.route('/profile') #profile page route 
def profile():
    if 'login_id' not in session: #checks if the login id is in sessions
        return redirect('/logout')
    data={
        'id':session['login_id']
    }
    login = Login.get_by_id(data) #grabs login information using login id from sessions
    followings = Login.loginsFollowings(data) #grabs how many users the login follows
    follows = Login.followsLogin(data) # grabs how many users follow the login
    return render_template('profile.html', login = login, num_of_following = len(followings), num_of_followers = len(follows) ) #connects html and brings in variables into html

@app.route('/update', methods =['POST']) # update profile method
def updateProfile():
    if 'login_id' not in session: #checks if the login id is in sessions
        return redirect('/logout')
    if not Login.validate_update(request.form): # if validation returns false (return to profile,flash messages)
        return redirect('/profile')
    password_hash = bcrypt.generate_password_hash(request.form['password']) #change password with new password by hashing new password 
    data ={
        'id': request.form['id'],
        'username': request.form['username'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'birthday': request.form['birthday'],
        'password': password_hash
    }
    Login.update(data) #updating login info with new form 
    return redirect('/homepage')

@app.route('/following') #followings route to see posts the login follows 
def Following():
    if 'login_id' not in session:#checks if the login id is in sessions
        return redirect('/logout')
    data={
        'id':session['login_id']
    }
    login = Login.get_by_id(data) #grabs login information using login id from sessions
    #this grabs all logins followers information with the amount of cheers each post has
    #and if the user has liked the post or not
    posts = Login.allLoginsFollowingWithCheerCount(data)  
    return render_template('following.html', login=login, posts = posts)


@app.route('/logout')
def logout():
    session.clear() # clears all data in sessions 
    return redirect('/login')