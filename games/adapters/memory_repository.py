from bisect import insort_left
from typing import List
import os
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Publisher, User, Review
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from pathlib import Path
from datetime import date, datetime
class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__games = list()
        self.__genres = list()
        self.__publishers = list()
        self.__users = list()
        self.__reviews = list()

    def add_game(self, game: Game):
        if isinstance(game, Game):
            insort_left(self.__games, game)
            for genre in game.genres:
                self.add_genre(genre)
            self.add_publisher(game.publisher)

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre) and genre not in self.__genres:
            self.__genres.append(genre)

    def add_publisher(self, publisher):
        if isinstance(publisher, Publisher) and publisher not in self.__publishers:
            self.__publishers.append(publisher)

    def add_user(self, user):
        if isinstance(user, User) and user not in self.__users:
            self.__users.append(user)

    def get_games(self) -> List[Game]:
        return self.__games
    
    def get_game(self, game_id: int) -> Game:
        for game in self.__games:
            if game.game_id == game_id:
                return game
        
    def get_number_of_games(self) -> int:
        return len(self.__games)
    
    def get_all_genres(self) -> List[Genre]:
        return self.__genres
    
    def get_number_of_genres(self) -> int:
        return len(self.__genres)
    
    def get_publishers(self) -> List[Publisher]:
        return self.__publishers
    
    def get_number_of_publishers(self) -> int:
        return len(self.__publishers)
    
    def get_users(self) -> List[User]:
        return self.__users
    
    def get_number_of_users(self) -> int:
        return len(self.__users)
    
    def get_user(self, username):
        for user in self.__users:
            print(user)
            if user.username == username:
                return user

    def add_review(self, review: Review):
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews
    
    def update_review(self, updated_review: Review):
        for index, review in enumerate(self.__reviews):
            if review.user.username == updated_review.user.username and review.game.game_id == updated_review.game.game_id:
                self.__reviews[index] = updated_review
    
    def add_to_user_wishlist(self, user: User, game: Game):
        user.favourite_games.append(game)
    
    def remove_from_wishlist(self, user: User, game: Game):
        user.favourite_games.remove(game)

def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(dir_name, "data/games.csv")
    reader = GameFileCSVReader(games_file_name)

    reader.read_csv_file() 
    games = reader.dataset_of_games

    for game in games:
        repo.add_game(game)
        for genre in game.genres:
            repo.add_genre(genre)
        repo.add_publisher(game.publisher)

