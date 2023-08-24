from library.db.models import User


def test_new_user():
    user = User("email@gmail.com", "password123", False, False, True, True)
    assert user.email == "email@gmail.com"
    assert user.hash_password != "password123"
    assert user.isPatient == True


def test_new_user_with_fixture(new_user):
    assert new_user.email == "email@gmail.com"
    assert new_user.hash_password != "password123"
    assert new_user.isPatient == True
