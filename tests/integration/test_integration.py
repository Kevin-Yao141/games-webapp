import pytest
from games import create_app



@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True
    })
    return my_app.test_client()


def test_browse_games(client):
    with client:
        # test the route without parameters
        response = client.get('/browse')
        assert response.status_code == 200

        # test the route with page parameter
        response = client.get('/browse?page=1')
        assert response.status_code == 200

        # test the route with genres parameter
        response = client.get('/browse?genres=Action')
        assert response.status_code == 200

        # test the route with publisher parameter
        response = client.get('/browse?publisher=Activision')
        assert response.status_code == 200

        # test the route with publisher and genres parameter
        response = client.get('/browse?genres=Action&publisher=Activision')
        assert response.status_code == 200

        # test the route with invalid parameters
        response = client.get('/browse?page=-1')
        assert response.status_code == 400

        # test the route with invalid genres parameter
        response = client.get('/browse?genres=Invalid')
        assert response.status_code == 400

        # test the route with invalid publisher parameter
        response = client.get('/browse?publisher=Invalid')
        assert response.status_code == 400

        # test the route with invalid publisher and genres parameter
        response = client.get('/browse?genres=Invalid&publisher=Invalid')
        assert response.status_code == 400

        # test the route with invalid page and genres parameter
        response = client.get('/browse?page=-1&genres=Invalid')
        assert response.status_code == 400

        # test the route with invalid page and publisher parameter
        response = client.get('/browse?page=-1&publisher=Invalid')
        assert response.status_code == 400

        # test the route with invalid page, genres and publisher parameter
        response = client.get('/browse?page=-1&genres=Invalid&publisher=Invalid')
        assert response.status_code == 400

        # test the route with valid and invalid genres parameter
        response = client.get('/browse?genres=Action,Invalid')
        assert response.status_code == 400
        
        # test the route with valid and invalid publisher parameter
        response = client.get('/browse?publisher=Activision,Invalid')
        assert response.status_code == 400
        
        # test the route with non-integer page parameter
        response = client.get('/browse?page=abc')
        assert response.status_code == 400
        
        # test the route with floating-point page parameter
        response = client.get('/browse?page=1.5')
        assert response.status_code == 400
        
        # test the route with zero page parameter
        response = client.get('/browse?page=0')
        assert response.status_code == 400


def test_home_page(client):
    with client:
        response = client.get('/')
        assert response.status_code == 200


def test_description_page(client):
    with client:

        # test the route with valid game_id
        response = client.get('/browse/7940')
        assert response.status_code == 200

        # test the route with invalid game_id
        response = client.get('/browse/Invalid')
        assert response.status_code == 404

        # test the route with invalid integer input
        response = client.get('/browse/123')
        assert response.status_code == 404


def test_login_page(client):
    with client:
        response = client.get('/login')
        assert response.status_code == 200


def test_register_page(client):
    with client:
        response = client.get('/signup')
        assert response.status_code == 200


