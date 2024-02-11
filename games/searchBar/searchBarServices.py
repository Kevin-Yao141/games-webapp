from games.adapters.repository import AbstractRepository

def get_games(repo:AbstractRepository):
    try:
        games = repo.get_games()
    except Exception:
        return {}
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
    return game_dicts

def search_games(query, repo:AbstractRepository):
    games = get_games(repo)
    filtered_games = [game for game in games if query.lower() in game['title'].lower()]
    return filtered_games


