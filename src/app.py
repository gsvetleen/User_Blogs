from src.common.database import Database
from src.models.user import User

__author__ = 'Svetleen'

from flask import Flask, render_template, request, session

# __name__ builtin variable for private variable in python -> contains '__main__'
app = Flask(__name__)
app.secret_key = "Svetleen"


@app.before_first_request
def initialize_databse():
    Database.initialize()

# @app.route('/')
# def home_template():
#     return render_template('home.html')

@app.route('/login')  # 127.0.0.1:5000/login
def login_template():
    return render_template('login.html')


@app.route('/register')  # 127.0.0.1:5000/register
def register_template():
    return render_template('register.html')


def initialize_database():
    Database.initialize()


# gets email and password and log the user in if they are valid
@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None

    # can give more and more data to the render template
    return render_template("profile.html", email=session['email'])


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    User.register(email, password)

    return render_template("profile.html", email=session['email'])



@app.route('/blogs/<string:user_id>')
def user_blogs(user_id):
    user = User.get_by_id(user_id)
    blogs = user.get_blogs()

    return render_template("user_blogs.html",blogs=blogs)

if __name__ == '__main__':
    app.run()
    # can modify port number
    # app.run(port=4995, debug=True)
