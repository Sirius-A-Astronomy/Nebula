from nebula import create_app


def test_config():
    """
    Tests if the create_app function actually properly enables the testing
    environment when it is specified.
    """
    assert not create_app().testing
    assert create_app(config_environment='testing').testing


def test_template(client):
    """
    Basic test which checks if the root page exists and is an HTML document.
    This serves more as an example test than as an actual test.
    """
    response = client.get('/')
    assert response.status_code == 200  # correct status
    assert b'<!DOCTYPE html>' in response.data  # response is an HTML document
