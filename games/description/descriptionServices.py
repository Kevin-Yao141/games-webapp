from games.adapters.repository import AbstractRepository
from games.authentication.services import UnknownUserException
from games.domainmodel.model import User, Game,  Review
from games.utilities.services import make_review

def get_game(repo: AbstractRepository, game_id):
    return repo.get_game(game_id)


def add_review(game_id: int, review_text: str, rating: int, username: str, repo: AbstractRepository):
    game = repo.get_game(game_id)
    if not game:
        raise ValueError("Game not found!")

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException
    
    existing = check_existing_review(game.reviews, username)
    review = make_review(review_text, user, game, rating)
    if not existing:
        print("yes")
        repo.add_review(review)
        user.add_review(review)
        game.add_review(review)
    else: 
        print("no")
        existing.comment = review_text
        existing.rating = rating
        repo.update_review(existing)


def get_favourite_games(repo: AbstractRepository, username):
    if username is None:
        return []
    user = repo.get_user(username)
    return user.favourite_games


def check_existing_review(review_list: [Review], username: str):
    print(f"Searching for reviews by {username} in {len(review_list)} reviews.")
    for review in review_list:
        print(f"Checking review by {review.user.username}")
        if review.user.username == username:
            print("Match found!")
            return review
    print("No match found!")
    return None


def calculate_average_rating(repo, game_id):
    game = repo.get_game(game_id)
    if not game:
        raise ValueError("Game not found!")
    if not game.reviews:
        return 0
    return sum([int(review.rating) for review in game.reviews]) / len(game.reviews)

