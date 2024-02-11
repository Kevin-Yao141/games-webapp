from sqlalchemy import select, inspect

from games.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['game_genres', 'games', 'genres', 'publishers', 'reviews, user_games_association', 'users']

def test_database_populate_select_all_genres(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table genres
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['genre_name'])

        assert all_genre_names == ['Action', 'Adventure', 'Stealth', 'Horror']

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['username'])

        assert all_users == ['thome', 'thorke']

def test_database_populate_select_all_reviews(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table revuews
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:
            all_reviews.append((row['timestamp'], row['comment'], row['rating'], row['game'], row['user']))

        assert all_reviews == [("2023-10-16", 12140 , 5, 'Hes just like me for real','thome'),
                                ("2023-10-16", 1172470 , 1, '**** this game!','throke')]

def test_database_populate_select_all_publishers(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_publishers_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table publishers
        select_statement = select([metadata.tables[name_of_publishers_table]])
        result = connection.execute(select_statement)

        all_publishers = []
        for row in result:
            all_publishers.append(row['publisher_name'])
        
        assert all_publishers == [("Bandai Namco Entertainment")]



def test_database_populate_select_all_games(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_articles_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_articles_table]])
        result = connection.execute(select_statement)

        all_games = []
        for row in result:
            all_games.append((row['game_id'], row['game_title'], row['price'], row['release_date'], row['description'], row['image_url'],row['website_url'], row['video_url'], row['publisher']))

        
        assert all_games == [(12140, "Max Payne", 3.49, "Jan 6, 2011", "Max Payne is a man with nothing to lose in the violent, cold urban night. A fugitive undercover cop framed for murder, hunted by cops and the mob, Max is a man with his back against the wall, fighting a battle he cannot hope to win. Prepare for pain…","https://cdn.akamai.steamstatic.com/steam/apps/12140/header.jpg?t=1618852800", "http://www.rockstargames.com/maxpayne/")]




