from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game

def get_number_of_games(repo: AbstractRepository):
    return repo.get_number_of_games()

def get_games(repo: AbstractRepository):
    games = repo.get_games()
    game_dicts = []
    for game in games:
        game_dict = {
            'game_id': game.game_id,
            'image': game.image_url,
            'title': game.title,
            'release_date': game.release_date,
            'price': game.price,
            'genres': [genre.genre_name for genre in game.genres],
            'publisher': game.publisher.publisher_name
        }
        game_dicts.append(game_dict)
    res = sorted(game_dicts, key=lambda x: x['title'])
    return res

def get_items(repo, offset, per_page):
    games = get_games(repo)
    return games[offset: offset + per_page]

def get_game(game_id, repo):
    game = repo.get_game(game_id)
    if game is None:
        return None
    return game

def get_genres(repo):
    genres = repo.get_all_genres()
    return genres

def get_publishers(repo):
    publishers = repo.get_publishers()
    return publishers

def get_games_by_genre(selected_genres, repo):
    games = get_games(repo)
    if len(selected_genres) == 1:
        filtered_games = [game for game in games if selected_genres[0] in game['genres']]
        return filtered_games
    else:
        filtered_games = [game for game in games if len(game['genres']) == 2 and all(genre in selected_genres for genre in game['genres'])]
    return filtered_games

def get_games_by_publisher(selected_publisher, repo):
    games = get_games(repo)
    filtered_games = [game for game in games if game['publisher'] == selected_publisher]

    return filtered_games

def get_games_by_genre_and_publisher(selected_genres, selected_publisher, repo):
    genre_games = get_games_by_genre(selected_genres, repo)
    filtered_games = [game for game in genre_games if game['publisher'] == selected_publisher]

    return filtered_games

