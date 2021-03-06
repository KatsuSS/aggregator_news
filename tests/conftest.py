from app.app import create_app
import pytest


@pytest.fixture
def app():
    app = create_app()
    app.client = app.test_client()
    yield app

