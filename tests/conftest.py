import os
import pytest

from library.app import create_app
from library.db.models import User
from library.db.db import db


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
    app = create_app()
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


@pytest.fixture(scope="session")
def test_db():
    return db


@pytest.fixture(scope='module')
def new_user():
    user = User("email@gmail.com", "password123", False, False, True, True)
    return user
