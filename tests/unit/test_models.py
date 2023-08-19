from library.db.models import User
import pytest

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