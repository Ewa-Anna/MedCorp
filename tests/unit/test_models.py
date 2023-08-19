import pytest

from library.db.models import User, Profile
from library.db.db import db

from library import app


def test_new_user():
    user = User("email@gmail.com", "password123", False, False, True, True)
    assert user.email == "email@gmail.com"
    assert user.password == "password123"
    assert user.isPatient == True


@pytest.fixture(scope='module')
def new_user():
    user = User("email@gmail.com", "password123", False, False, True, True)
    return user


def test_new_user_with_fixture(new_user):
    assert new_user.email == "email@gmail.com"
    assert new_user.password == "password123"
    assert new_user.isPatient == True


@pytest.fixture(scope='module')
def test_db():
    db.init_app(app)
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='module')
def test_profile(test_db):
    profile = Profile(_id=1, name="Patient", surname="Example")
    test_db.session.add(profile)
    test_db.session.commit()
    return profile