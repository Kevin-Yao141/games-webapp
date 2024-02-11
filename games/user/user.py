from flask import Blueprint, render_template, abort, session, redirect, url_for, request
import games.adapters.repository as repo
from games.utilities.services import get_user, remove_from_wishlist
from games.authentication.authentication import login_required
from games.description.description import remove_from_wishlist
from games.utilities.services import get_user

user_blueprint = Blueprint('user_bp', __name__)


@user_blueprint.route('/profile', methods=['GET'])
@login_required
def user():
    username = session['username']
    username = username.lower().strip()
    user = get_user(username, repo.repo_instance)
    return render_template("/user/user.html", user=user)


@user_blueprint.route('/profile', methods=['POST'])
@login_required
def remove_from_wishlist_endpoint():
    username = session['username']
    username = username.lower().strip()
    game_id = int(request.form['game_id'])
    remove_from_wishlist(game_id, username, repo.repo_instance)
    return redirect(url_for('user_bp.user'))


