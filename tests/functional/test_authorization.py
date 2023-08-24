from library.db.models import User
from flask_login import login_user

def test_not_a_doctor_authorization(app, client):
    test_user = User(email="not@adoctor.com", password="123", isAdmin=False, isDoctor=False, isPatient=True, isActive=True)

    with app.app_context(), app.test_request_context():
        client.login_user(test_user)
        response = client.get("/create_app")
        
    assert response.status_code == 403 # Status: forbidden

def test_actual_doctor_autorization(client):
    test_user = User(email="actually@adoctor.com", password="123", isAdmin=False, isDoctor=True, isPatient=True, isActive=True)

    with client:
        client.login_user(test_user)
        response = client.get("/create_app")

    assert response.status_code == 200 # Status: OK
