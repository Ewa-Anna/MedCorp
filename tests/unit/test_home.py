from bs4 import BeautifulSoup
from flask import url_for

def test_home_template(app, client):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for("pages.home"))
        assert response.status_code == 200

        soup = BeautifulSoup(response.data, "html.parser")

        tag = soup.find("h3")
        assert tag is not None

        text = "Welcome to MedCorp! How can we help you?"
        assert tag.get_text() == text