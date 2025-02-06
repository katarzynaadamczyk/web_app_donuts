'''
test if correct data is in database
if so scraper works correctly
'''
from app.utils import get_all_available_donuts, get_all_available_manufacturers
from sqlalchemy import select, and_
from app.models import *
import pytest


def test_get_all_available_manufacturers_returns_3_manufacturers(app_with_db):
    '''
    testing if get_all_available_manufacturers returns 3 manufacturers as in database.json
    '''
    with app_with_db.app_context():
        manufacturers = get_all_available_manufacturers()
        assert len(manufacturers) == 3

        assert set(['Putka', 'Oskroba', 'Grzybki']) == set([item[1] for item in manufacturers])


def test_get_all_available_donuts(app_with_db):
    '''
    testing if get_all_available_donuts returns 16 donuts
    '''
    with app_with_db.app_context():
        donuts = get_all_available_donuts()
        assert len(donuts) == 16


def test_get_correct_donuts_parameters_for_Putka(app_with_db):
    '''
    testing if correct donuts parameters are in db
    for Putka donuts
    '''
    with app_with_db.app_context():
        stmt = select(Donuts.name, Donuts.kcal, Donuts.weight, Manufacturers.name)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Putka'))
        results = db.session.execute(stmt).all()
        assert len(results) == 8
        
        stmt = select(Donuts.name, Donuts.kcal, Donuts.weight, Manufacturers.name)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Putka', Donuts.name == 'Pączek Wyborowy 75 g'))
        results = db.session.execute(stmt).all()
        assert len(results) == 1
        assert results[0][0] == 'Pączek Wyborowy 75 g'
        assert results[0][1] == 241.5
        assert results[0][2] == 75
        assert results[0][3] == 'Putka'

        stmt = select(Donuts.name, Donuts.kcal, Donuts.weight, Manufacturers.name)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Putka', Donuts.name == 'Pączek Słony Karmel 90g'))
        results = db.session.execute(stmt).all()
        assert len(results) == 1
        assert results[0][0] == 'Pączek Słony Karmel 90g'
        assert results[0][1] == 329.4
        assert results[0][2] == 90
        assert results[0][3] == 'Putka'
                        

def test_get_correct_donuts_parameters_for_Oskroba(app_with_db):
    '''
    testing if correct donuts parameters are in db
    for Oskroba donuts
    '''
    with app_with_db.app_context():
        stmt = select(Donuts.name, Donuts.kcal, Donuts.weight, Manufacturers.name)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Oskroba'))
        results = db.session.execute(stmt).all()
        assert len(results) == 5
        
        stmt = select(Donuts.name, Donuts.kcal, Donuts.weight, Manufacturers.name)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Oskroba', Donuts.name == 'Pączek'))
        results = db.session.execute(stmt).all()
        assert len(results) == 1
        assert results[0][0] == 'Pączek'
        assert results[0][1] == 234.5
        assert results[0][2] == 70
        assert results[0][3] == 'Oskroba'

        stmt = select(Donuts.name, Donuts.kcal, Donuts.weight, Manufacturers.name)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Oskroba', Donuts.name == 'Pączek z bitą śmietaną'))
        results = db.session.execute(stmt).all()
        assert len(results) == 1
        assert results[0][0] == 'Pączek z bitą śmietaną'
        assert results[0][1] == 282.8
        assert results[0][2] == 70
        assert results[0][3] == 'Oskroba'

def test_get_correct_donuts_parameters_for_Grzybki(app_with_db):
    '''
    testing if correct donuts parameters are in db
    for Oskroba donuts
    '''
    with app_with_db.app_context():
        stmt = select(Donuts.name, Donuts.kcal, Donuts.weight, Manufacturers.name)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Grzybki'))
        results = db.session.execute(stmt).all()
        assert len(results) == 3
        
        stmt = select(Donuts.name, Donuts.kcal, Donuts.weight, Manufacturers.name)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Grzybki', Donuts.name == 'Pączek z pistacją'))
        results = db.session.execute(stmt).all()
        assert len(results) == 1
        assert results[0][0] == 'Pączek z pistacją'
        assert results[0][1] == 397
        assert results[0][2] == 100
        assert results[0][3] == 'Grzybki'

        stmt = select(Donuts.name, Donuts.kcal, Donuts.weight, Manufacturers.name)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Grzybki', Donuts.name == 'Pączek'))
        results = db.session.execute(stmt).all()
        assert len(results) == 1
        assert results[0][0] == 'Pączek'
        assert results[0][1] == 407
        assert results[0][2] == 100
        assert results[0][3] == 'Grzybki'

