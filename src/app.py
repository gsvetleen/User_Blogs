from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User

__author__ = 'Svetleen'

from flask import Flask, render_template, request, session, make_response

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
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()
    return render_template("user_blogs.html", blogs=blogs, email=user.email)


@app.route('/posts/new', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_blog.html', blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])

        new_post = Post(blog_id, title, content, user.email)
        new_post.save_to_mongo()
        # return render_template('user_blogs')
        return make_response(blog_posts(user._id))


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])

        new_blog = Blog(user.email, title, description, user._id)
        new_blog.save_to_mongo()
        # return render_template('user_blogs')
        return make_response(user_blogs(user._id))


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('posts.html', posts=posts, blog_title=blog.title, blog_id=blog._id)


if __name__ == '__main__':
    app.run()
    # can modify port number
    # app.run(port=4995, debug=True)
