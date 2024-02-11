from flask import Blueprint, render_template, redirect, url_for, abort, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from password_validator import PasswordValidator
import games.adapters.repository as repo
from games.authentication import services
from functools import wraps

login_blueprint = Blueprint('login_bp', __name__)
signup_blueprint = Blueprint('signup_bp', __name__)
logout_blueprint = Blueprint('logout_bp', __name__)

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form =  LoginForm()
    username_not_recognised = None
    password_not_recognised = None

    try:
        if form.validate_on_submit():
            username = form.user_name.data.strip().lower()
            user = services.get_user(username, repo.repo_instance)

            services.authenticate_user(user['username'], form.password.data, repo.repo_instance)


            session.clear()
            session['username'] = user['username']
            return redirect(url_for('home_bp.home'))
    except services.UnknownUserException:
        username_not_recognised = "User does not exist!"
    
    except services.AuthenticationException:
        password_not_recognised = "Incorrect username or password!"
    
    return render_template("authentication/authentication.html", title="Log In", form=form, 
                           username_not_recognised =username_not_recognised, 
                           password_not_recognised = password_not_recognised)

@signup_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()

    if form.validate_on_submit():
        services.add_user(form.user_name.data, form.password.data, repo.repo_instance)
        return redirect(url_for('login_bp.login'))
    
    return render_template("authentication/authentication.html",
                            title="Sign Up", 
                            form=form, 
                            handler_url = url_for('signup_bp.signup'))

@logout_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))

class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Your user name is required'),
        Length(min=3, message='Your user name is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    user_name = StringField('Username', [
        DataRequired(message='Your user name is required'),
    ]
    )
    password = PasswordField('Password', [
        DataRequired(message='Your password is required')
    ])
    submit = SubmitField('Log In')

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session['username']:
            return redirect(url_for('login_bp.login'))
        return view(**kwargs)
    return wrapped_view