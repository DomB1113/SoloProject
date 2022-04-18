
from flask_app.models.post import Post
from flask_app.models.login import Login
from flask_app import app
from flask import redirect, request, session, render_template, flash

@app.route('/likepost', methods = ['POST'])
def likePost():
    if 'login_id' not in session:
        return redirect('/logout')
    data = {
        'post_id':request.form['post_id'],
        'login_id':request.form['login_id']
    }
    Post.likePost(data)
    return redirect('/homepage')

@app.route('/unlikepost', methods = ['POST'])
def unlikePost():
    if 'login_id' not in session:
        return redirect('/logout')
    data = {
        'post_id':request.form['post_id'],
        'login_id':request.form['login_id']
    }
    Post.unlikePost(data)
    return redirect('/homepage')

@app.route('/likepost/following', methods = ['POST'])
def likePostfollowing():
    if 'login_id' not in session:
        return redirect('/logout')
    data = {
        'post_id':request.form['post_id'],
        'login_id':request.form['login_id']
    }
    Post.likePost(data)
    return redirect('/following')

@app.route('/unlikepost/following', methods = ['POST'])
def unlikePostfollowing():
    if 'login_id' not in session:
        return redirect('/logout')
    data = {
        'post_id':request.form['post_id'],
        'login_id':request.form['login_id']
    }
    Post.unlikePost(data)
    return redirect('/following')

@app.route('/view/post/<int:id>')
def viewPost(id):
    if 'login_id' not in session:
        return redirect('/logout')
    login_data={
        'id':session['login_id']
    }
    login = Login.get_by_id(login_data) 
    data={
        'id':session['login_id'],
        'post_id': id
    }
    post = Post.viewPostWithLoginWithCheers(data)
    return render_template('view_post.html', post = post, login=login)

@app.route('/likepost/viewing', methods = ['POST'])
def likeViewedPost():
    if 'login_id' not in session:
        return redirect('/logout')
    data = {
        'post_id':request.form['post_id'],
        'login_id':request.form['login_id']
    }
    Post.likePost(data)
    return redirect(f"/view/post/{request.form['post_id']}")

@app.route('/unlikepost/viewing', methods = ['POST'])
def unlikeViewedPost():
    if 'login_id' not in session:
        return redirect('/logout')
    data = {
        'post_id':request.form['post_id'],
        'login_id':request.form['login_id']
    }
    Post.unlikePost(data)
    return redirect(f"/view/post/{request.form['post_id']}")

@app.route('/follow/user', methods = ["POST"])
def follow_user():
    data ={
        'login_id': request.form['login_id'],
        'following_id': request.form['following_id']
    }
    Login.FollowUser(data)
    return redirect('/homepage')

@app.route('/unfollow', methods = ["POST"])
def unfollow_user():
    data ={
        'followings_id': request.form['followings_id']
    }
    Login.unFollowUser(data)
    return redirect('/following')

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
    print(request.form)
    data = {
        'title' : request.form['title'],
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