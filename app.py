import os
from flask import Flask, request, render_template, redirect, session
from lib.database_connection import get_flask_database_connection
from lib.database_connection import DatabaseConnection
from user import User
from user_repository import UserRepository

from lib.space_repository import SpaceRepository
from lib.space import Space

# Create a new Flask app
app = Flask(__name__)

app.secret_key = "some_really_secret_key"


# == Your Routes Here ==

# GET /spaces - list all spaces
# Try it:
#   ; open http://localhost:5001/index
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')
@app.route('/spaces', methods=['GET'])
def get_spaces():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    spaces = repository.all() 
    return render_template('spaces/index.html', spaces=spaces)

# GET /spaces/new - show the form
@app.route('/spaces/new', methods=['GET'])
def new_space():
    return render_template('spaces/new.html')

#POST /spaces - create a space
@app.route('/spaces', methods=['POST'])
def create_space():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    space = Space(None, request.form['name'], request.form['description'], request.form['price'], session['user_id'])
    repository.create(space)
    return redirect('/spaces')

@app.route('/test', methods=['GET'])
def get_test():
    return render_template('test.html')




@app.route('/users', methods=['POST'])
def create_user():
    connection = DatabaseConnection()
    connection.connect()
    user_repository = UserRepository(connection)
    user_details = request.form
    user = User(username=user_details["username"], password=user_details["password"])
    user_repository.create(user)
    return redirect("/index")


@app.route('/login', methods=['GET'])
def get_login_form():
    connection = DatabaseConnection()
    connection.connect()
    return render_template("login.html")


@app.route('/sessions', methods=['POST'])
def create_session():
    connection = DatabaseConnection()
    connection.connect()
    user_repository = UserRepository(connection)

    username = request.form["username"]
    password = request.form["password"]

    user = user_repository.find_by_username(username)

    if user and user.password == password:
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect("/test")
    else:
        return redirect("/login")

    
# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
