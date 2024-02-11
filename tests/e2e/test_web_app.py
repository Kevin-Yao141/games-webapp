import pytest
from flask import session

from games import create_app
from games.adapters import memory_repository

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SESSION_COOKIE_SECURE': False,  # Disable secure cookies for testing
        'SESSION_COOKIE_HTTPONLY': True,  # Enable httpOnly cookies
    })

    return my_app.test_client()

def test_signup(client):
    response_code = client.get('/signup').status_code
    assert response_code == 200

    response = client.post(
        '/signup',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )

    assert response.headers['Location'] == '/login'  
 


def test_login(client, auth):
    response_code = client.get('/login').status_code
    assert response_code == 200

    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert session['username'] == 'gmichael'

