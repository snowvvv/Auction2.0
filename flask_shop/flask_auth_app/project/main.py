from flask import Blueprint, render_template
from . import db, app
from flask_auth_app import project


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')


if __name__ == "__main__":
    app.run(debug=True)
