def test_home_page(app):
    with app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 200
        
        response = test_client.post('/nonexistent')
        assert response.status_code == 404