import os
import tempfile
import pytest
from app import create_app
from app.db import Base, _engine

@pytest.fixture(scope="session")
def app():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

    app = create_app("config.DevConfig")

    with app.app_context():
        engine = _engine()
        Base.metadata.create_all(engine)

    yield app

    try:
        os.remove(db_path)
    except OSError:
        pass

@pytest.fixture()
def client(app):
    return app.test_client()
    
