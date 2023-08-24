from bs4 import BeautifulSoup
from flask import url_for

def test_about_page(app, client):
    with app.app_context(), app.test_request_context():
        response = client.get(url_for("pages.about"))
        assert response.status_code == 200

        soup = BeautifulSoup(response.data, "html.parser")

        tag = soup.find("h5")
        assert tag is not None

        text = "Sources"
        assert tag.get_text() == text