from flask.cli import FlaskGroup

from app import create_app, db
from app.models import *


app = create_app()
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
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
