import imp
from flask_app import app
from flask_app.controllers import logins,posts


if __name__ == "__main__":
    app.run(debug=True)