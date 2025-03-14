from flask.cli import FlaskGroup

from app import create_app, db
from app.models import Donuts, Manufacturers
from app.utils import load_data_from_json


app = create_app()
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    app.db.drop_all()
    app.db.create_all()
    app.db.session.commit()


@cli.command("add_json_to_db")
def add_json_to_db():
    load_data_from_json("./database.json")
    db.session.commit()


@cli.command("putka")
def seed_db():
    db.session.add(Manufacturers(name="Putka"))
    db.session.commit()


@cli.command("donut")
def seed_db():
    db.session.add(Donuts(name="Pączek", kcal=500, weight=80, manufacturer_id=1))
    db.session.commit()


if __name__ == "__main__":
    cli()
