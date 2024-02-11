from flask import abort, render_template, Blueprint, request, redirect, session
from flask_paginate import Pagination
import games.adapters.repository as repo
from games.browse import browseServices
from games.domainmodel.model import Genre
browse_blueprint = Blueprint(
    'games_bp', __name__)

@browse_blueprint.route('/browse', methods=['GET'])
def browse_games():
    all_genres = browseServices.get_genres(repo.repo_instance)
    all_genre_names = [genre.genre_name for genre in all_genres]
    all_publishers = browseServices.get_publishers(repo.repo_instance)
    all_publisher_names = [publisher.publisher_name for publisher in all_publishers]
    per_page = 5
    page = (request.args.get('page', 1))
    try:
        page = int(page)
    except ValueError:
        abort(400, description=f"The page number must be an integer.")
    offset = (page - 1) * per_page
    selected_genres = request.args.get('genres')
    selected_publisher = request.args.get('publisher')
    total_games = 0

    if selected_publisher:
        if selected_publisher not in all_publisher_names:
            abort(400, description=f"{selected_publisher} is not a valid publisher.")
    if selected_genres:
        selected_genres = selected_genres.split(',')
        for genre in selected_genres:
                if genre not in all_genre_names:
                    abort(400, description=f"{genre} is not a valid genre.")
        
    if selected_genres and selected_publisher:
        games = browseServices.get_games_by_genre_and_publisher(selected_genres, selected_publisher, repo.repo_instance)[offset: offset + per_page]
        total_games = len(browseServices.get_games_by_genre_and_publisher(selected_genres, selected_publisher, repo.repo_instance))
    elif selected_genres:
        games = browseServices.get_games_by_genre(selected_genres, repo.repo_instance)[offset: offset + per_page]
        total_games = len(browseServices.get_games_by_genre(selected_genres, repo.repo_instance))
    elif selected_publisher:
        games = browseServices.get_games_by_publisher(selected_publisher, repo.repo_instance)[offset: offset + per_page]
        total_games += len(browseServices.get_games_by_publisher(selected_publisher, repo.repo_instance))
    else:
        games = browseServices.get_items(repo.repo_instance, offset, per_page)
        total_games = browseServices.get_number_of_games(repo.repo_instance)
        
    if page < 1 or page > total_games//per_page + 1:
        abort(400, description=f"The page number must be positive and less than {total_games//per_page + 1}.")
    pagination = Pagination(page=page, per_page=per_page, total=total_games)

    
    return render_template(
        'browse/browse.html', games=games, pagination=pagination, genres=all_genres, publishers=all_publishers
    )
