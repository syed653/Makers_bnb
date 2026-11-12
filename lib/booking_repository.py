from lib.booking import Booking

class BookingRepository:
    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * FROM bookings')
        bookings = []
        for row in rows:
            booking = Booking(row["id"], row["space_id"], row["user_id"], row["date"])
            bookings.append(booking)
        return bookings

    def create(self, booking):
        self._connection.execute(
            'INSERT INTO bookings (space_id, user_id, date) VALUES (%s, %s, %s)',
            [booking.space_id, booking.user_id, booking.date]
        )
        return None

    def is_date_available(self, space_id, date):
        rows = self._connection.execute(
            "SELECT * FROM bookings WHERE space_id = %s AND date = %s AND status = 'confirmed'",
            [space_id, date]
        )
        return len(rows) == 0

    # Top half of the page: all bookings this user has made (their own requests)
    def find_by_user(self, user_id):
        rows = self._connection.execute(
            'SELECT * FROM bookings WHERE user_id = %s', [user_id]
        )
        bookings = []
        for row in rows:
            bookings.append(Booking(row["id"], row["space_id"], row["user_id"], row["date"], row["status"]))
        return bookings

    # Bottom half: pending requests for spaces this user OWNS
    def find_pending_by_owner(self, owner_id):
        rows = self._connection.execute(
            'SELECT bookings.* FROM bookings '
            'JOIN spaces ON bookings.space_id = spaces.id '
            "WHERE spaces.user_id = %s AND bookings.status = 'pending'",
            [owner_id]
        )
        bookings = []
        for row in rows:
            bookings.append(Booking(row["id"], row["space_id"], row["user_id"], row["date"], row["status"]))
        return bookings

    # Find one booking by id (used for the ownership check)
    def find(self, booking_id):
        rows = self._connection.execute(
            'SELECT * FROM bookings WHERE id = %s', [booking_id]
        )
        row = rows[0]
        return Booking(row["id"], row["space_id"], row["user_id"], row["date"], row["status"])

    # Approve / reject: change a booking's status
    def update_status(self, booking_id, status):
        self._connection.execute(
            'UPDATE bookings SET status = %s WHERE id = %s',
            [status, booking_id]
        )
        return None

        # Cancel a booking (delete it)
    def delete(self, booking_id):
        self._connection.execute(
            'DELETE FROM bookings WHERE id = %s', [booking_id]
        )
        return None