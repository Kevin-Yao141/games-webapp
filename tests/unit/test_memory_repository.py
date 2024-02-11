from games.adapters.memory_repository import MemoryRepository
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Publisher, Genre, Game
import pytest


@pytest.fixture
def game1():
    return Game(1, "g1")

@pytest.fixture
def genre1():
    return Genre("g1")

@pytest.fixture
def publisher1():
    return Publisher("p1")


def test_add_game(game1):
    repo = MemoryRepository()
    repo.add_game(game1)
    assert game1 in repo.get_games()

def test_add_genre(genre1):
    repo = MemoryRepository()
    repo.add_genre(genre1)
    assert genre1 in repo.get_all_genres()

def test_add_publisher(publisher1):
    repo = MemoryRepository()
    repo.add_publisher(publisher1)
    assert publisher1 in repo.get_publishers()

def test_get_games():
    repo = MemoryRepository()
    repo.add_game(Game(1, "g1"))
    expected_games = [Game(1, "g1")]
    assert repo.get_games() == expected_games

def test_get_number_of_games():
    repo = MemoryRepository()
    assert repo.get_number_of_games() == 0
    game_list = [Game(1, "g1"),Game(2,"a"),Game(3,"b"),Game(4,"c")]
    for game in game_list:
        repo.add_game(game)
    assert repo.get_number_of_games() == 4

def test_get_all_genres():
    repo = MemoryRepository()
    repo.add_genre(Genre("g1"))
    expected_genres = [Genre("g1")]
    assert repo.get_all_genres() == expected_genres

def test_get_number_of_genres():
    repo = MemoryRepository()
    assert repo.get_number_of_genres() == 0
    genre_list = [Genre("a"),Genre("b"),Genre("c"),Genre("d"),Genre("e")]
    for genre in genre_list:
        repo.add_genre(genre)
    assert repo.get_number_of_genres() == 5

def test_get_publishers():
    repo = MemoryRepository()
    repo.add_publisher(Publisher("p1"))
    assert repo.get_publishers() == [Publisher("p1")]

def test_get_number_of_publishers():
    repo = MemoryRepository()
    assert repo.get_number_of_publishers() == 0
    pub_list = [Publisher("a"), Publisher("b"), Publisher("c")]
    for pub in pub_list:
        repo.add_publisher(pub)
    assert repo.get_number_of_publishers() == 3







