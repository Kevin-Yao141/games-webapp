from flask import blueprints, jsonify 
import games.adapters.repository as repo
from games.searchBar import searchBarServices as searchBarServices
search_blueprint = blueprints.Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/search/<query>', methods=['GET'])
def search_games(query):
    search_results = searchBarServices.search_games(query, repo.repo_instance)
    return jsonify(search_results)
