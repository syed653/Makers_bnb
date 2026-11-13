from lib.booking_repository import BookingRepository

def test_booking_inside_range_is_created(web_client, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    with web_client.session_transaction() as session:
        session['user_id'] = 1
    web_client.post('/spaces/1/bookings', data={'date': '2026-12-15'})
    bookings = BookingRepository(db_connection).all()
    assert len(bookings) == 1      # in-range date → booking saved

def test_booking_outside_range_is_rejected(web_client, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    with web_client.session_transaction() as session:
        session['user_id'] = 1
    web_client.post('/spaces/1/bookings', data={'date': '2027-06-15'})
    bookings = BookingRepository(db_connection).all()
    assert len(bookings) == 0      # out-of-range date → nothing saved