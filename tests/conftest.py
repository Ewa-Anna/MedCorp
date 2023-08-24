import os
import pytest

from library.app import create_app
from library.db.models import User, Profile


@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def client(app):
    app.config["TESTING"] = True
    client = app.test_client()
    return client


@pytest.fixture(scope='module')
def test_client(app):
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def test_profile(test_db):
    profile = Profile(_id=1, name="Patient", surname="Example")
    test_db.session.add(profile)
    test_db.session.commit()
    return profile


@pytest.fixture(scope='module')
def new_user():
    user = User("email@gmail.com", "password123", False, False, True, True)
    return user
