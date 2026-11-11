from lib.booking_repository import BookingRepository
from lib.booking import Booking

def test_create_adds_a_booking(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = BookingRepository(db_connection)
    repository.create(Booking(None, 1, 1, "2026-12-25"))
    bookings = repository.all()
    assert len(bookings) == 1
    assert bookings[0].space_id == 1

def test_date_is_available_when_free(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = BookingRepository(db_connection)
    assert repository.is_date_available(1, "2026-12-25") == True

def test_date_not_available_when_taken(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = BookingRepository(db_connection)
    repository.create(Booking(None, 1, 1, "2026-12-25"))
    assert repository.is_date_available(1, "2026-12-25") == False