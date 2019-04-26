import pytest

# Import app from file.
@pytest.fixture
def app():
    from restful_api_app import app
    return app

# Create test client for this app.
@pytest.fixture
def client(app):
    return app.test_client()