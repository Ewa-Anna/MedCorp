import os
from library import app
import pytest

@pytest.fixture(scope='module')
def test_client():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client