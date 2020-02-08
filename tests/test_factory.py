from nebula import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_template(client):
    response = client.get('/')
    assert response.status_code == 200  # correct status
    assert b'<!DOCTYPE html>' in response.data  # response is an HTML document
