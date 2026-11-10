import os
from flask import Flask, request, render_template, redirect, session
from lib.database_connection import get_flask_database_connection
from lib.space_repository import SpaceRepository
from lib.space import Space

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

# GET /spaces - list all spaces
# Try it:
#   ; open http://localhost:5001/index
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

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
