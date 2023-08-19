from library import app
import os

import pytest

@pytest.fixture(scope='module')
def test_home_page():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'

    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        assert b"Welcome" in response.data
        
        response = test_client.post('/')
        assert response.status_code == 405
        assert b"Flask Error" not in response.data