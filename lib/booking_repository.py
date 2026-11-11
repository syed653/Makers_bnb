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
            'SELECT * FROM bookings WHERE space_id = %s AND date = %s',
            [space_id, date]
        )
        return len(rows) == 0