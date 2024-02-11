from flask import Blueprint, jsonify, render_template, abort, request, session, url_for, redirect, flash
from games.authentication.authentication import login_required
from games.description import descriptionServices
import games.adapters.repository as repo
import games.utilities.services as services
import games.utilities.services as services
from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired, NumberRange

description_blueprint = Blueprint('description_bp', __name__)

@description_blueprint.route('/browse/<int:game_id>', methods=['GET'])
def description(game_id):
    game = descriptionServices.get_game(repo.repo_instance, game_id)
    if game is None:
        abort(404, description="No game was found with the given id.")

    average_rating = descriptionServices.calculate_average_rating(repo.repo_instance, game_id)
    
    # Initialize the form only if the user is logged in
    if 'username' in session:
        form = CommentForm()
        user = services.get_user(session['username'], repo.repo_instance)
        favourite_games = user.favourite_games
    else:
        form = None
        favourite_games = []

    return render_template(
        "/description/description.html",
        game=game,
        form=form,
        favourite_games=favourite_games,
        average_rating=average_rating,
        handler_url=url_for('description_bp.add_review_endpoint', game_id=game_id)

    )

@description_blueprint.route('/browse/<int:game_id>/add_review', methods=['POST'])
@login_required
def add_review_endpoint(game_id):
    form = CommentForm()
    if form.validate_on_submit():
        username = session['username']
        descriptionServices.add_review(game_id, form.review.data, form.rating.data, username, repo.repo_instance)
    return redirect(url_for('description_bp.description', game_id=game_id))

@description_blueprint.route('/browse/<int:game_id>/add_to_wishlist', methods=['POST'])
@login_required
def add_to_wishlist_endpoint(game_id):
    username = session['username']
    add_to_wishlist(game_id, username, repo.repo_instance)
    return redirect(url_for('description_bp.description', game_id=game_id))


def add_to_wishlist(game_id, username, repo):
    """Adds a game to a user's wishlist."""
    services.add_to_wishlist(username, game_id, repo)
    
def remove_from_wishlist(game_id, username, repo):
    """Removes a game from a user's wishlist."""
    services.remove_from_wishlist(username, game_id, repo)


@description_blueprint.route('/browse/<int:game_id>/remove_from_wishlist', methods=['GET', 'POST'])
@login_required
def remove_from_wishlist_endpoint(game_id):
    username = session['username']
    services.remove_from_wishlist(username, game_id, repo.repo_instance)
    return redirect(url_for('description_bp.description', game_id=game_id))


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)
        

class CommentForm(FlaskForm):
    rating = IntegerField('Rating (out of 5)', validators=[InputRequired(), NumberRange(min=1, max=5)])
    review = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    game_id = HiddenField("Game id")
    submit = SubmitField('Submit')