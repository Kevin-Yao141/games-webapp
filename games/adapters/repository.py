import abc
from typing import List

from games.domainmodel.model import Game, User, Publisher, Genre

repo_instance = None

class RepositoryException(Exception):
    def __init__(self, message = None):
        print(f"repositoryException: {message}")

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_game(self, game: Game):
        raise NotImplementedError

    @abc.abstractmethod
    def get_games(self) -> List[Game]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_users(self) -> List[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_publisher(self, publisher: Publisher):
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError
    
    @abc.abstractmethod
    def add_to_user_wishlist(self, user: User, game: Game):
        raise NotImplementedError
    
    @abc.abstractmethod
    def remove_from_wishlist(self, user: User, game: Game):
        raise NotImplementedError