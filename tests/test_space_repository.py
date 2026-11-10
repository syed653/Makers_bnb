from lib.space_repository import SpaceRepository
from lib.space import Space

def test_all_returns_all_spaces(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = SpaceRepository(db_connection)
    spaces = repository.all()
    assert len(spaces) == 2  # however many your seed inserts

def test_create_adds_a_space(db_connection):
    db_connection.seed("seeds/makers_bnb.sql")
    repository = SpaceRepository(db_connection)
    new_space = Space(None, "Treehouse", "Up in the leaves", 50, 1)
    repository.create(new_space)
    spaces = repository.all()
    assert len(spaces) == 3
    assert spaces[-1].name == "Treehouse"