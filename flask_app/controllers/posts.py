
from flask_app.models.post import Post
from flask_app.models.login import Login
from flask_app import app
from flask import redirect, request, session, render_template, flash


@app.route('/post')
def post():
    if 'login_id' not in session:
        return redirect('/logout')
    data={
        'id':session['login_id']
    }
    login = Login.get_by_id(data) 
    return render_template('create_post.html', login = login)

@app.route('/create/post', methods=['POST'])
def createPost():
    if 'login_id' not in session:
        return redirect('/logout')
    data = {
        'upload_photo' : request.form['upload_photo'],
        'description' : request.form['description'],
        'login_id': session['login_id']
    }
    Post.create_post(data)
    return redirect('/your/posts')

@app.route('/your/posts')
def yourPosts():
    if 'login_id' not in session:
        return redirect('/logout')
    data={
        'id':session['login_id']
    }
    login_data = {
        'login_id': session['login_id']
    }
    login = Login.get_by_id(data) 
    posts = Post.yourPosts(login_data)
    return render_template('your_posts.html', login = login, posts = posts)

@app.route('/delete/post/<int:id>')
def deletePost(id):
    data= {
        'id':id
    }
    Post.deletePost(data)
    return redirect('/your/posts')