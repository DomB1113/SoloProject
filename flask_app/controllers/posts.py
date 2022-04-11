from flask_app.models.login import Login
from flask_app import app
from flask import redirect, request, session, render_template, flash


@app.route('/post')
def post():
    return render_template('create_post.html')