from app import app
from lib.database_connection import DatabaseConnection
from playwright.sync_api import Page, expect


def test_auth_integration(web_client, db_connection):
    db_connection.execute("TRUNCATE TABLE bookings, users, spaces;")
    db_connection.execute("INSERT INTO users (username, password) VALUES ('test', '1234');")
    response = web_client.post('/sessions', data={
    'username': 'test',
    'password': '1234'
})

    assert response.status_code == 302
    assert response.headers['Location'] == '/spaces'

def test_auth_playwright(page: Page, test_web_address, db_connection):
    db_connection.execute("TRUNCATE TABLE bookings, users, spaces;")
    db_connection.execute("INSERT INTO users (username, password) VALUES ('test', '1234');")

    page.goto(f"http://{test_web_address}/login")
    page.get_by_label("Username").fill("test")
    page.get_by_label("Password").fill("1234")
    page.get_by_role("button").click()

    expect(page).to_have_url(f"http://{test_web_address}/spaces")