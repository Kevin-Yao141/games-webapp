import csv
from pathlib import Path
from datetime import date, datetime

from werkzeug.security import generate_password_hash

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Publisher

def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of  the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row

def load_games_genres_and_publishers(data_path: Path, repo: AbstractRepository, database_mode: bool):
    genres = dict()

    games_filename = str(data_path / "games.csv")
    for data_row in read_csv_file(games_filename):

        game = Game(game_id = int(data_row[0]), game_title = data_row[1])
        game.release_date = data_row[2]
        game.price = float(data_row[3])
        game.description = data_row[4]
        game.image_url = data_row[7]
        game.website_url = data_row[8]
        game.video_url = data_row[21]
        game.screenshot = data_row[20]

        publisher = Publisher(publisher_name = data_row[16])
        repo.add_publisher(publisher)
        game.publisher = publisher


        genre_names = data_row[18].split(",")
        for genre_name in genre_names:
            genre = Genre(genre_name.strip())
            game.add_genre(genre)
            repo.add_genre(genre)

        repo.add_game(game)

