'''
create table in db
'''
from app import db

class Donuts(db.Model):
    __tablename__ = "donuts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    kcal = db.Column(db.Float(5), nullable=False)
    weight = db.Column(db.Float(5), nullable=False)
    manufacturer_id = db.Column(db.Integer, nullable=False)

    def __init__(self, name, kcal, weight, manufacturer_id):
        self.name = name
        self.kcal = kcal
        self.weight = weight
        self.manufacturer_id = manufacturer_id


class Manufacturers(db.Model):
    __tablename__ = "manufacturers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name
