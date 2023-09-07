import pytest

from library.app import create_app
from library.db.models import User
from library.db.db import db


@pytest.fixture(scope='module')
def app():
    app = create_app('test')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope='module')
def client(app):
    app.config["TESTING"] = True
    client = app.test_client()
    return client


@pytest.fixture(scope='module')
def new_user():
    user = User("email@gmail.com", "password123", False, False, True, True)
    return user
