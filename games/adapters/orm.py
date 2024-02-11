from sqlalchemy import (
    PrimaryKeyConstraint, Table, MetaData, Column, Integer, String, Float, DateTime, Date, Text,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from games.domainmodel.model import Game, Genre, Publisher, User, Review, Wishlist

# global variable giving access to the MetaData (schema) information of the database
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('username', String(20), primary_key=True, unique=True, nullable=False),
    Column('password', String(20), nullable=False)
)

games_table = Table(
    'games', metadata, 
    Column('game_id', Integer, primary_key=True, autoincrement=True),
    Column('game_title', Text, nullable=True),
    Column('price', Float, nullable=True),
    Column('release_date', String(50), nullable=False),
    Column('description', Text, nullable=True),
    Column('image_url', String(255), nullable=True),
    Column('website_url', String(255), nullable=True),
    Column('video_url', String(255), nullable=True),
    Column('publisher', ForeignKey('publishers.publisher_name'))
)

genres_table = Table(
    'genres', metadata, 
    #Column('genre_id', Integer, primary_key=True, autoincrement=True),
    Column('genre_name', String(64), primary_key=True, nullable=False)
)

game_genres_table = Table(
    'game_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('game_id', ForeignKey('games.game_id')),
    Column('genre_id', ForeignKey('genres.genre_name')),
)

publishers_table = Table(
    'publishers', metadata,
    Column('publisher_name', String(64), primary_key=True),
)


reviews_table = Table(
    'reviews', metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),
    Column('timestamp', DateTime, nullable=False),
    Column('comment', String(255), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('game', ForeignKey('games.game_id')),
    Column('user', ForeignKey('users.username')),
)

user_games_association = Table(
    'user_games_association', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', ForeignKey('users.username')),
    Column('game_id', ForeignKey('games.game_id')),
)


def map_model_to_tables():
    mapper(User, users_table, properties={
        '_User__username': users_table.c.username,
        '_User__password': users_table.c.password,
            '_User__reviews': relationship(Review, back_populates='_Review__user', foreign_keys=[reviews_table.c.user]),
        '_User__favourite_games': relationship(Game, secondary=user_games_association, back_populates='_Game__users')
    })

    mapper(Game, games_table, properties={
        '_Game__game_id': games_table.c.game_id,
        '_Game__game_title': games_table.c.game_title,
        '_Game__price': games_table.c.price,
        '_Game__release_date': games_table.c.release_date,
        '_Game__description': games_table.c.description,
        '_Game__image_url': games_table.c.image_url,
        '_Game__website_url': games_table.c.website_url,
        '_Game__video_url': games_table.c.video_url,
        '_Game__publisher_name': games_table.c.publisher,
        '_Game__reviews': relationship(Review, back_populates='_Review__game', foreign_keys=[reviews_table.c.game]),
        '_Game__genres': relationship(Genre, secondary=game_genres_table),
        '_Game__publisher': relationship(Publisher, foreign_keys=[games_table.c.publisher]),
        '_Game__users': relationship(User, secondary=user_games_association, back_populates='_User__favourite_games')
    })


    mapper(Genre, genres_table, properties={
        '_Genre__genre_name': genres_table.c.genre_name,

    })

    mapper(Publisher, publishers_table, properties={
        '_Publisher__publisher_name': publishers_table.c.publisher_name,

    })

    mapper(Review, reviews_table, properties={
        '_Review__timestamp': reviews_table.c.timestamp,
        '_Review__comment': reviews_table.c.comment,
        '_Review__rating': reviews_table.c.rating,
        '_Review__game_id': reviews_table.c.game,
        '_Review__username': reviews_table.c.user,
        '_Review__game': relationship(Game, foreign_keys=[reviews_table.c.game]),
        '_Review__user': relationship(User, foreign_keys=[reviews_table.c.user]),

    })