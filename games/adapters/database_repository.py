from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session

from games.domainmodel.model import Game, Genre, Publisher, User, Review, Wishlist
from games.adapters.repository import AbstractRepository


class SessionContextManager:

    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
         self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
         self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()
        
    def add_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()
    
    def add_multiple_genres(self, genres: List[Genre]):
        return 0
    
    def get_reviews_for_games(self, game_id: int) -> List[Review]:
        return 0
    
    def get_reviews_for_user(self, user_id: int) -> List[Review]:
        reviews = self._session_cm.session.query(User).filter
        return reviews
    
    def search_games_by_title(self, title_string: str) -> List[Game]:
        games = self._session_cm.session.query(Game).filter(Game._Game__game_title.like(f"%{title_string}%")).all()
        return games
    
    def search_games_by_publisher(self, publisher_name: str) -> List[Game]:
        games = self._session_cm.session.query(Game).filter(Game._Game__publisher.like(f"%{publisher_name}%")).all()
        return games

    def search_games_by_genre(self, genre_name: str) -> List [Game]:
        games = self._session_cm.session.query(Game).filter(Game._Game__genres.like(f"%{genre_name}%")).all()
        return games
    def get_number_of_games(self):
        number_of_games = self._session_cm.session.query(Game).count()
        return number_of_games
    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.merge(publisher)
            scm.commit()
    
    def add_review(self, review: Review):
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_games(self, sorting: bool= False) -> List[Game]:
        games = self._session_cm.session.query(Game).all()
        return games
    
    def get_game(self, game_id: int) -> Game:
        game = None
        try:
            game = self._session_cm.session.query(Game).filter(Game._Game__game_id == game_id).one()
        except NoResultFound:
            print(f'Game {game_id} was not found')
        
        return game
        
    def get_all_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        return genres
        
    def get_publishers(self) -> List[Publisher]:
        publishers = self._session_cm.session.query(Publisher).all()
        return publishers
        
    def get_users(self) -> List[User]:
        users = self._session_cm.session.query(User).all()
        return users
    
    def get_user(self, username):
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__username == username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user
        
    def get_reviews(self) -> List[Review]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews
    
    def add_to_user_wishlist(self, user: User, game: Game):
        with self._session_cm as scm:
            user.favourite_games.append(game)  # Add game to user's wishlist
            scm.session.merge(user)     # Merge updated user into the session
            scm.commit()                # Commit changes to the database


    def remove_from_wishlist(self, user: User, game: Game):
        with self._session_cm as scm:
            user.favourite_games.remove(game)
            scm.session.merge(user)
            scm.commit()
        

        