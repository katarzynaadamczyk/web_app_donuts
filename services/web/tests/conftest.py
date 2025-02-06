'''
create testing client
'''
import pytest
from app import create_app, db
from app.models import *
from app.utils import load_data_from_json



@pytest.fixture(scope='session')
def app_with_db():
    app = create_app()
    app.config.update({
        "TESTING": True,  
        "SQLALCHEMY_DATABASE_URI": "postgresql://user:password@localhost/test_db",  # Użyj testowej bazy danych
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.create_all()
        load_data_from_json("./database.json")
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app_with_db):
    # create testing client
    with app_with_db.test_client() as client:
        yield client


@pytest.fixture
def runner(app_with_db):
    # Tworzymy CLI runner do testowania komend CLI
    return app_with_db.test_cli_runner()


