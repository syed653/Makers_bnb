from app import app
from lib.database_connection import DatabaseConnection
from playwright.sync_api import Page


def test_auth_integration():
    client = app.test_client()
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users, spaces;")
    connection.execute("INSERT INTO users (username, password) VALUES ('test', '1234');")
    response = client.post('/login', data={
        'username': 'test',
        'password': '1234'
    })

def test_auth_playwright(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users, spaces;")
    connection.execute("INSERT INTO users (username, password) VALUES ('test', '1234');")

    page.goto("http://127.0.0.1:5001/login")
    page.get_by_label("Username").fill("test")
    page.get_by_label("Password").fill("1234")
    page.get_by_role("button").click()

    assert page.url == "http://127.0.0.1:5001/test"