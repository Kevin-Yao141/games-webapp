from games.adapters.repository import AbstractRepository
from games.domainmodel.model import User
from werkzeug.security import generate_password_hash, check_password_hash

def get_users(repo: AbstractRepository):
    return repo.get_users()

def get_user(username:str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException
    return user_to_dict(user)

def add_user(username, password, repo: AbstractRepository):
    user = repo.get_user(username)
    if user is not None:
        raise ValueError('User already exists')

    else:
        user = User(username, generate_password_hash(password))
        repo.add_user(user)


def authenticate_user(username, password, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(username)
    if user is not None:
        authenticated = check_password_hash(user.password, password)

    if not authenticated:
        raise AuthenticationException


class UnknownUserException(Exception):
    pass

class AuthenticationException(Exception):
    pass

def user_to_dict(user: User):
    user_dict = {
        'username': user.username,
        'password': user.password
    }
    return user_dict


