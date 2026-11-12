from lib.booking_repository import BookingRepository
from lib.booking import Booking

def test_owner_sees_pending_requests(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repo = BookingRepository(db_connection)
    repo.create(Booking(None, 1, 2, "2026-12-15"))   
    pending = repo.find_pending_by_owner(1)            
    assert len(pending) == 1
    assert pending[0].space_id == 1

def test_owner_can_approve(web_client, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repo = BookingRepository(db_connection)
    repo.create(Booking(None, 1, 2, "2026-12-15"))
    booking = repo.find_by_user(2)[0]
    with web_client.session_transaction() as session:
        session['user_id'] = 1                        
    response = web_client.post(f'/bookings/{booking.id}/approve')
    assert response.status_code == 302
    assert repo.find(booking.id).status == "confirmed"

def test_non_owner_cannot_approve(web_client, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repo = BookingRepository(db_connection)
    repo.create(Booking(None, 1, 2, "2026-12-15"))
    booking = repo.find_by_user(2)[0]
    with web_client.session_transaction() as session:
        session['user_id'] = 2                         
    response = web_client.post(f'/bookings/{booking.id}/approve')
    assert response.status_code == 403
    assert repo.find(booking.id).status == "pending"   