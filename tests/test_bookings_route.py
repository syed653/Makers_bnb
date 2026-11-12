from app import app

def test_booking_inside_range_succeeds(web_client, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    with web_client.session_transaction() as session:
        session['user_id'] = 1
    response = web_client.post('/spaces/1/bookings', data={'date': '2026-12-15'})
    assert response.status_code == 302 

def test_booking_outside_range_is_rejected(web_client, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    with web_client.session_transaction() as session:
        session['user_id'] = 1
    response = web_client.post('/spaces/1/bookings', data={'date': '2027-06-15'})
    assert response.status_code == 400 