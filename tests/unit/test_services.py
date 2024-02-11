import pytest
from games.utilities import services
from games.domainmodel.model import Game, Genre, Publisher, User, Review
from games.adapters.memory_repository import MemoryRepository
from games.adapters.repository import AbstractRepository
from games.browse import browseServices as browseServices
from games.description import descriptionServices
from games.searchBar import searchBarServices as searchBarServices
from games.authentication import services as auth_services

@pytest.fixture
def test_game():
    test_game = Game(2020, "Test Game")
    test_game.add_genre(Genre("Test Genre"))
    test_game.add_genre(Genre("Test Genre 2"))
    test_game.publisher = Publisher("Test Publisher")
    return test_game


@pytest.fixture
def test_repo(test_game, test_user):
    repo = MemoryRepository()
    repo.add_game(test_game)
    repo.add_user(test_user)
    return repo

@pytest.fixture
def test_user():
    user = User("tester", "Password123")
    return user

# tests for getting games
def test_get_games(test_repo):
    assert test_repo.get_games()[0].title == browseServices.get_games(test_repo)[0]["title"]

# tests for getting number of games
def test_get_number_of_games(test_repo):
    assert len(browseServices.get_games(test_repo)) == 1

# tests for getting genres
def test_get_all_genres(test_repo):
    assert len(browseServices.get_genres(test_repo)) == 2

# tests for getting publishers
def test_get_publishers(test_repo):
    assert len(browseServices.get_publishers(test_repo)) == 1


# tests for getting games by genre
def test_get_games_by_genre(test_repo, test_game):
    selected_genres = ["Test Genre"]
    games = browseServices.get_games_by_genre(selected_genres, test_repo)
    assert games[0]['title'] == test_game.title


# tests for getting games by publisher
def test_get_games_by_publisher(test_repo, test_game):
    assert test_game.title == browseServices.get_games_by_publisher("Test Publisher", test_repo)[0]["title"]

# tests for getting games by genre and publisher
def test_get_games_by_genre_and_publisher(test_repo, test_game):
    selected_genres = ["Test Genre"]
    assert test_game.title == browseServices.get_games_by_genre_and_publisher(selected_genres, "Test Publisher", test_repo)[0]["title"]

# tests for getting items
def test_get_items(test_repo, test_game):
    assert test_game.title == browseServices.get_items(test_repo, 0, 1)[0]["title"]

# test for invalid genre
def test_get_games_by_invalid_genre(test_repo):
    selected_genres = ["Invalid Genre"]
    assert len(browseServices.get_games_by_genre(selected_genres, test_repo)) == 0

# test for invalid publisher
def test_get_games_by_invalid_publisher(test_repo):
    assert len(browseServices.get_games_by_publisher("Invalid Publisher", test_repo)) == 0


# test for invalid genre and publisher
def test_get_games_by_invalid_genre_and_publisher(test_repo):
    selected_genres = ["Invalid Genre"]
    assert len(browseServices.get_games_by_genre_and_publisher(selected_genres, "Invalid Publisher", test_repo)) == 0

# test for invalid offset
def test_get_items_invalid_offset(test_repo):
    assert len(browseServices.get_items(test_repo, 100, 1)) == 0

# test for invalid per_page
def test_get_items_invalid_per_page(test_repo):
    assert len(browseServices.get_items(test_repo, 0, 100)) == 1

# test for negative offset
def test_get_items_negative_offset(test_repo):
    assert len(browseServices.get_items(test_repo, -1, 1)) == 0

# test for negative per_page
def test_get_items_negative_per_page(test_repo):
    assert len(browseServices.get_items(test_repo, 0, -1)) == 0


# test for zero per_page and offset
def test_get_items_zero_per_page_and_offset(test_repo):
    assert len(browseServices.get_items(test_repo, 0, 0)) == 0

'''

Tests for descriptionServices.py

'''

# tests for getting game
def test_get_game(test_repo, test_game):
    assert descriptionServices.get_game(test_repo, 2020).title == test_game.title

# tests for getting game with invalid id
def test_get_game_invalid_id(test_repo):
    assert descriptionServices.get_game(test_repo, 1000) is None

def test_add_review(test_repo, test_game, test_user):
    descriptionServices.add_review(test_game.game_id, "test", 5, test_user.username, test_repo)
    assert test_game.reviews[0].comment == "test"

def test_add_review_invalid_game(test_repo, test_user):
    with pytest.raises(ValueError):
        descriptionServices.add_review(None, "test", 5, test_user.username, test_repo)

def test_get_favourite_games(test_repo, test_user):
    username = test_user.username
    assert len(descriptionServices.get_favourite_games(test_repo, username)) == len(test_user.favourite_games)

def test_get_favourite_games_invalid_user(test_repo):
    assert len(descriptionServices.get_favourite_games(test_repo, None)) == 0

def test_calculate_average_rating(test_repo, test_game):
    assert descriptionServices.calculate_average_rating(test_repo, test_game.game_id) == 0

def test_calculate_average_rating_invalid_game(test_repo):
    with pytest.raises(ValueError):
        descriptionServices.calculate_average_rating(test_repo, None)

def test_check_existing_review(test_game, test_user):
    review = Review(test_user, test_game, 5, "test", None)
    test_game.add_review(review)
    assert descriptionServices.check_existing_review(test_game.reviews, test_user.username) == review

def test_check_existing_review_invalid_review(test_game, test_user):
    assert descriptionServices.check_existing_review(test_game.reviews, test_user.username) is None

def test_check_existing_review_invalid_user(test_game):
    assert descriptionServices.check_existing_review(test_game.reviews, None) is None


'''
Testing for searchServices.py

'''

# tests for getting games
def test_get_games(test_repo, test_game):
    assert searchBarServices.get_games(test_repo)[0]["title"] == test_game.title

# tests for searching games
def test_search_games(test_repo, test_game):
    assert searchBarServices.search_games("test", test_repo)[0]["title"] == test_game.title

# tests for searching games with invalid query
def test_search_games_invalid_query(test_repo):
    assert len(searchBarServices.search_games("invalid", test_repo)) == 0

# tests for searching games with empty query
def test_search_games_empty_query(test_repo):
    assert len(searchBarServices.search_games("", test_repo)) == len(test_repo.get_games())

# tests for searching games with whitespace query
def test_search_games_whitespace_query(test_repo):
    assert len(searchBarServices.search_games(" ", test_repo)) == len(test_repo.get_games())

# tests for searching games with invalid repo
def test_search_games_invalid_repo():
    assert len(searchBarServices.search_games("test", None)) == 0


''' testing for authenticationservices.py'''

# tests for registering user

def test_get_user(test_repo):
    user = auth_services.get_user("tester", test_repo)
    assert user["username"] == "tester"

def test_get_user_invalid_username(test_repo):
    with pytest.raises(auth_services.UnknownUserException):
        auth_services.get_user("invalid", test_repo)

def test_add_user(test_repo):
    auth_services.add_user("test", "test", test_repo)
    assert auth_services.get_user("test", test_repo)["username"] == "test"

def test_add_user_existing_user(test_repo):
    with pytest.raises(ValueError):
        auth_services.add_user("tester", "test", test_repo)


def test_authenticate_user_invalid_username(test_repo):
    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user("invalid", "invalid", test_repo)

def test_authenticate_user_invalid_password(test_repo, test_user):
    user_dict = auth_services.user_to_dict(test_user)
    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(user_dict["username"], "invalid", test_repo)


'''
Testing utlities.py
'''

def test_get_game(test_game, test_repo):
    game_id = test_game.game_id
    game = services.get_game(game_id, test_repo)
    assert game == test_game

def test_get_game_invalid_id(test_repo):
    assert services.get_game(1000, test_repo) is None

def test_get_users(test_repo, test_user):
    assert services.get_users(test_repo)[0] == test_user

def test_get_user(test_repo, test_user):
    assert services.get_user("tester", test_repo) == test_user


def test_get_user_invalid_username(test_repo):
    with pytest.raises(auth_services.UnknownUserException):
        services.get_user("invalid", test_repo)


def test_add_to_wishlist(test_repo, test_user, test_game):
    services.add_to_wishlist("tester", test_game.game_id, test_repo)
    assert test_game in test_user.favourite_games


def test_remove_from_wishlist(test_repo, test_user, test_game):
    services.remove_from_wishlist("tester", test_game.game_id, test_repo)
    assert test_game not in test_user.favourite_games


def test_make_review(test_repo, test_user, test_game):
    review = services.make_review("test", test_user, test_game, 5)
    assert review.comment == "test"
    assert review.user == test_user
    assert review.game == test_game
    assert review.rating == 5

def test_make_review_invalid_rating(test_repo, test_user, test_game):
    with pytest.raises(ValueError):
        services.make_review("test", test_user, test_game, 6)

def test_make_review_negative_rating(test_repo, test_user, test_game):
    with pytest.raises(ValueError):
        services.make_review("test", test_user, test_game, -1)

def test_make_review_invalid_user(test_repo, test_user, test_game):
    with pytest.raises(ValueError):
        services.make_review("test", None, test_game, 5)
    
def test_make_review_invalid_game(test_repo, test_user, test_game):
    with pytest.raises(ValueError):
        services.make_review("test", test_user, None, 5)
    
    
