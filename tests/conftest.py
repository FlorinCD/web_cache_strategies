import pytest
from app.app import create_app


# fixture instance of the app
@pytest.fixture(scope="function")
def app_instance():
    app = create_app()
    yield app


# fixture to simulate the client locally - no need to run the server
@pytest.fixture(scope="function")
def client_cleared_cache(app_instance):
    app_instance.cache.clear()
    client = app_instance.test_client()
    yield client

