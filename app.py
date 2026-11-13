import os
from flask import Flask, request, render_template, redirect, session, flash
from lib.database_connection import get_flask_database_connection
from lib.database_connection import DatabaseConnection
from user import User
from user_repository import UserRepository
from lib.space_repository import SpaceRepository
from lib.space import Space
from lib.booking_repository import BookingRepository
from lib.booking import Booking
from lib.login_required import login_required
from datetime import datetime
import random

# Create a new Flask app
app = Flask(__name__)

app.secret_key = "some_really_secret_key"


# == Your Routes Here ==

# GET /spaces - list all spaces
# Try it:
#   ; open http://localhost:5001/index
@app.route("/", methods=["GET"])
def index():
    # connection = get_flask_database_connection(app)
    # spaces = SpaceRepository(connection).all()
    delay = random.randint(2, 3)
    return render_template("index.html", delay=delay)

@app.route('/index', methods=['GET'])
def get_index():
    # connection = get_flask_database_connection(app)
    # spaces = SpaceRepository(connection).all()
    delay = random.randint(2, 3)
    return render_template('index.html', delay=delay)

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
    space = Space(None, request.form['name'], request.form['description'], request.form['price'], session['user_id'], request.form['available_from'], request.form['available_to'])
    repository.create(space)
    return redirect('/spaces')

# POST /spaces/<id>/bookings — request a booking
# POST /spaces/<id>/bookings — request a booking
@app.route('/spaces/<int:id>/bookings', methods=['POST'])
@login_required
def create_booking(id):
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    space_repository = SpaceRepository(connection)

    date = request.form['date']
    space = space_repository.find(id)

    if space.available_from is None or space.available_to is None:
        flash("Sorry, this space has no available dates set.")
        return redirect(f'/spaces/{id}')

    requested = datetime.strptime(date, "%Y-%m-%d").date()
    if requested < space.available_from or requested > space.available_to:
        flash("Sorry, that date is outside this space's available dates.")
        return redirect(f'/spaces/{id}')

    if not booking_repository.is_date_available(id, date):
        flash("Sorry, that date is already booked for this space.")
        return redirect(f'/spaces/{id}')

    booking = Booking(None, id, session['user_id'], date)
    booking_repository.create(booking)
    return redirect(f'/spaces/{id}')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/login')

@app.route('/test', methods=['GET'])
def get_test():
    return render_template('test.html')

# GET /spaces/<id> — show one space
@app.route('/spaces/<int:id>', methods=['GET'])
def get_space(id):
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    space = repository.find(id)
    return render_template('spaces/show.html', space=space)

# GET /signup — show the sign up form
@app.route('/signup', methods=['GET'])
def get_signup():
    return render_template('signup.html')

# GET /bookings — my requests (top) + requests for my spaces (bottom)
@app.route('/bookings', methods=['GET'])
@login_required
def get_bookings():
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    space_repository = SpaceRepository(connection)
    user_repository = UserRepository(connection)

    user_id = session['user_id']

    # Top half: my own requests (attach each space so we can show its name)
    my_requests = []
    for booking in booking_repository.find_by_user(user_id):
        space = space_repository.find(booking.space_id)
        my_requests.append({'booking': booking, 'space': space})

    # Bottom half: pending requests for spaces I own
    owner_requests = []
    for booking in booking_repository.find_pending_by_owner(user_id):
        space = space_repository.find(booking.space_id)
        requester = user_repository.find(booking.user_id)
        owner_requests.append({'booking': booking, 'space': space, 'requester': requester})

    return render_template('bookings/index.html',
                           my_requests=my_requests,
                           owner_requests=owner_requests)

# POST /bookings/<id>/approve — owner approves a request
@app.route('/bookings/<int:id>/approve', methods=['POST'])
@login_required
def approve_booking(id):
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    space_repository = SpaceRepository(connection)

    booking = booking_repository.find(id)
    space = space_repository.find(booking.space_id)

    # Only the owner of the space can approve
    if space.user_id != session['user_id']:
        return "You can only approve requests for your own spaces.", 403

    booking_repository.update_status(id, 'confirmed')
    return redirect('/bookings')


# POST /bookings/<id>/reject — owner rejects a request
@app.route('/bookings/<int:id>/reject', methods=['POST'])
@login_required
def reject_booking(id):
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)
    space_repository = SpaceRepository(connection)

    booking = booking_repository.find(id)
    space = space_repository.find(booking.space_id)

    # Only the owner of the space can reject
    if space.user_id != session['user_id']:
        return "You can only reject requests for your own spaces.", 403

    booking_repository.update_status(id, 'denied')
    return redirect('/bookings')

# POST /bookings/<id>/cancel — guest cancels their own request
@app.route('/bookings/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_booking(id):
    connection = get_flask_database_connection(app)
    booking_repository = BookingRepository(connection)

    booking = booking_repository.find(id)

    # Only the person who made the booking can cancel it
    if booking.user_id != session['user_id']:
        return "You can only cancel your own bookings.", 403

    booking_repository.delete(id)
    return redirect('/bookings')




@app.route('/users', methods=['POST'])
def create_user():
    connection = get_flask_database_connection(app)
    user_repository = UserRepository(connection)
    user_details = request.form
    user = User(username=user_details["username"], password=user_details["password"])
    error = user_repository.create(user)
    if error:
        return render_template("signup.html", error=error)
    return redirect("/index")


@app.route('/login', methods=['GET'])
def get_login_form():
    connection = DatabaseConnection()
    connection.connect()
    return render_template("login.html")


@app.route('/sessions', methods=['POST'])
def create_session():
    connection = get_flask_database_connection(app)
    connection.connect()
    user_repository = UserRepository(connection)

    username = request.form["username"]
    password = request.form["password"]

    user = user_repository.find_by_username(username)

    if user and user.password == password:
        session["user_id"] = user.id
        session["username"] = user.username
        return redirect("/spaces")
    else:
        return render_template("login.html", error="Incorrect username or password")

@app.route('/test', methods=['GET'])
def homepage():
    return render_template('test_new.html')

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
