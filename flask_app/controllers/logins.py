from flask_app.models.login import Login
from flask_app import app
from flask import redirect, request, session, render_template, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods = ['POST'])
def register():
    if not Login.validate_registration(request.form):
        return redirect('/')
    password_hash = bcrypt.generate_password_hash(request.form['password'])
    print(password_hash)
    data ={
        'username': request.form['username'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'birthday': request.form['birthday'],
        'password': password_hash
    }
    
    login_id =Login.insert(data)
    session['login_id'] = login_id

    return redirect('/homepage')

@app.route('/login', methods =['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    login_data = Login.get_by_email(data)
    if not login_data:
        flash('Invalid Email Address or Password', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(login_data.password, request.form['password']):
        flash('Invalid Email Address or Password', 'login')
        return redirect('/')
    session['login_id'] = login_data.id
    return redirect('/homepage')

@app.route('/homepage')
def homepage():
    if 'login_id' not in session:
        return redirect('/logout')
    data={
        'id':session['login_id']
    }
    login = Login.get_by_id(data) 
    return render_template('homepage.html' , login = login)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')