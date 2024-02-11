from games.adapters.repository import AbstractRepository
from games.authentication.services import UnknownUserException
from games.domainmodel.model import User, Game,  Review
from datetime import datetime

def get_game(game_id, repo):
    game = repo.get_game(game_id)
    if game is None:
        return None
    return game

def get_users(repo: AbstractRepository):
    return repo.get_users()

def get_user(username:str, repo: AbstractRepository) -> User:
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException
    return user
   

def add_to_wishlist(username, game_id, repo: AbstractRepository):
    user = get_user(username, repo)
    game = get_game(game_id, repo)
    repo.add_to_user_wishlist(user, game)    
    
    try:
        user = get_user(username, repo)
        game = get_game(game_id, repo)
    except:
        raise ValueError("Invalid username or game id")
    user.add_favourite_game(game)


def remove_from_wishlist(username, game_id, repo: AbstractRepository):
    user = get_user(username, repo)
    game = get_game(game_id, repo)
    repo.remove_from_wishlist(user, game)

def make_review(review_text: str, user: User, game: Game, rating: int):
    timestamp = datetime.today()
    review = Review(user, game, rating, review_text, timestamp)

    return review
