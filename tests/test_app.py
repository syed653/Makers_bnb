from playwright.sync_api import Page, expect

# Tests for your routes go here

"""
We can render the index page
"""

def test_get_index(page, test_web_address):
    # We load a virtual browser and navigate to the /index page
    page.goto(f"http://{test_web_address}/index")

    # We assert that it has the text "This is the homepage."
    expect(page.locator("h1")).to_have_text("Lions BnB")


def test_get_spaces_lists_them(page, test_web_address, db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    page.goto(f"http://{test_web_address}/spaces")
    h2_tags = page.locator("h2")
    expect(h2_tags).to_have_count(2)