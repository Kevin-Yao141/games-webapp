from pathlib import Path

from games.adapters.repository import AbstractRepository
from games.adapters.csv_data_importer import load_games_genres_and_publishers

def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    load_games_genres_and_publishers(data_path, repo, database_mode)
