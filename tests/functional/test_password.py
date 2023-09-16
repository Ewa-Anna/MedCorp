from library.db.models import User
from library.db.db import db


def test_correct_password(app):
    test_user = User(email="example@example.com", password="123", isAdmin=False, isDoctor=False, isPatient=True, isActive=True)
    db.session.add(test_user)
    db.session.commit()

    with app.test_client() as client:
        response = client.post("/login", data={"email": test_user.email, "password": "123"},  follow_redirects=True)
        assert response.status_code == 200


def test_incorrect_password(app):
    test_user = User(email="example2@example.com", password="123", isAdmin=False, isDoctor=False, isPatient=True, isActive=True)
    db.session.add(test_user)
    db.session.commit()

    with app.test_client() as client:
        response = client.post("/login", data={"email": test_user.email, "password": "321"},  follow_redirects=True)
        assert response.status_code == 200 # even is password is incorrect the website response is OK, as it rendered properly
        assert b"Email or password is not correct." in response.data

