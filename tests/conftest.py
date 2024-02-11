import pytest

from games import create_app
from games.adapters import memory_repository





@pytest.fixture
def in_memory_repo():
    repo = memory_repository.MemoryRepository()
    memory_repository.populate(repo)

    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'WTF_CSRF_ENABLED': False,                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='gmichael', password='CarelessWhisper1984'):
        return self.__client.post(
            '/login',
            data={'user_name': user_name, 'password': password}
        )
    

    def logout(self):
        return self.__client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
