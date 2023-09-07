from library.db.models import User
from library.db.db import db


def test_not_a_doctor_authorization(app):
    test_user = User(email="not@adoctor.com", password="123", isAdmin=False, isDoctor=False, isPatient=True, isActive=True)
    db.session.add(test_user)
    db.session.commit()
    assert User.query.count() == 1

    with app.test_client() as client:
        response = client.post("/login", data={"email": test_user.email, "password": "123"})
        assert response.status_code == 200

        response = client.get("/create_app")
        assert response.status_code == 403


def test_actual_doctor_autorization(app):
    test_user = User(email="actually@adoctor.com", password="123", isAdmin=False, isDoctor=True, isPatient=True, isActive=True)
    db.session.add(test_user)
    db.session.commit()

    with app.test_client() as client:
        response = client.post("/login", data={"email": test_user.email, "password": "123"},  follow_redirects=True)
        assert response.status_code == 200

        response = client.get("/create_app")
        assert response.status_code == 200
