'''
test if correct data is in database
if so scraper works correctly
'''

from app.utils_solver import Solver
from sqlalchemy import select, and_
from app.models import *
import pytest


def test_pick_me_donuts_unlimited_all_donuts_available(app_with_db):
    '''
    test pick me donuts unlimited - all donuts available
    '''
    solver = Solver()
    with app_with_db.app_context():
        stmt = select(Donuts.id, Donuts.weight, Donuts.kcal)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id))
        donuts = db.session.execute(stmt).all()
        results = solver.pick_me_donuts_unlimited(donuts, 200)

        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 814.00
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 1
        assert results[1] == {14: 2}
        
        results = solver.pick_me_donuts_unlimited(donuts, 250)

        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 975.40
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 2
        assert results[1] == {10: 2, 14: 1}


def test_pick_me_donuts_unlimited_only_Putka_donuts(app_with_db):
    '''
    test pick me donuts unlimited - only Putka donuts
    '''        
    solver = Solver()
    with app_with_db.app_context():
        stmt = select(Donuts.id, Donuts.weight, Donuts.kcal)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Putka'))
        donuts = db.session.execute(stmt).all()
        # first test
        results = solver.pick_me_donuts_unlimited(donuts, 200)
        
        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 694.20
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 1
        assert results[1] == {6: 3}

        # second test
        results = solver.pick_me_donuts_unlimited(donuts, 250)
        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 893.80
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 2
        assert results[1] == {4: 2, 6: 1}


def test_pick_me_donuts_unlimited_only_Oskroba_donuts(app_with_db):
    '''
    test pick me donuts unlimited - only Oskroba donuts
    '''   
    solver = Solver()
    with app_with_db.app_context():
        stmt = select(Donuts.id, Donuts.weight, Donuts.kcal)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Oskroba'))
        donuts = db.session.execute(stmt).all()
        # first test
        results = solver.pick_me_donuts_unlimited(donuts, 200)
        
        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 673.20
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 1
        assert results[1] == {12: 2}

        # second test
        results = solver.pick_me_donuts_unlimited(donuts, 250)

        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 957.40
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 2
        assert results[1] == {10: 1, 12: 2}


def test_pick_me_donuts_unlimited_only_Grzybki_donuts(app_with_db):
    '''
    test pick me donuts unlimited - only Grzybki donuts
    '''   
    solver = Solver()
    with app_with_db.app_context():
        stmt = select(Donuts.id, Donuts.weight, Donuts.kcal)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Grzybki'))
        donuts = db.session.execute(stmt).all()

        # first test
        results = solver.pick_me_donuts_unlimited(donuts, 200)

        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 814.00
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 1
        assert results[1] == {14: 2}
        
        # second test
        results = solver.pick_me_donuts_unlimited(donuts, 250)

        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 814.00
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 1
        assert results[1] == {14: 2}


def test_pick_me_donuts_0_1_all_donuts(app_with_db):
    '''
    test pick me donuts 0 1 - different versions
    '''
    solver = Solver()
    with app_with_db.app_context():
        stmt = select(Donuts.id, Donuts.weight, Donuts.kcal)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id))
        donuts = db.session.execute(stmt).all()
        # first test
        results = solver.pick_me_donuts_0_1(donuts, 200)
        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 813.00
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 2
        assert results[1] == {14: 1, 15: 1}

        # second test
        results = solver.pick_me_donuts_0_1(donuts, 250)
        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 974.00
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 3
        assert results[1] == {10: 1, 11: 1, 14: 1}


def test_pick_me_donuts_0_1_Putka_donuts(app_with_db):
    '''
    test pick me donuts 0 1 - only Putka Donuts
    '''
    solver = Solver()
    with app_with_db.app_context():        
        stmt = select(Donuts.id, Donuts.weight, Donuts.kcal)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Putka'))
        donuts = db.session.execute(stmt).all()

        # first test
        results = solver.pick_me_donuts_0_1(donuts, 200)
        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 665.20
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 2
        assert results[1] == {4: 1, 5: 1}

        # second test
        results = solver.pick_me_donuts_0_1(donuts, 250)

        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 892.00
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 3
        assert results[1] == {3: 1, 4: 1, 6: 1}



def test_pick_me_donuts_0_1_Oskroba_donuts(app_with_db):
    '''
    test pick me donuts 0 1 - only Oskroba Donuts
    '''
    solver = Solver()
    with app_with_db.app_context():     
        stmt = select(Donuts.id, Donuts.weight, Donuts.kcal)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Oskroba'))
        donuts = db.session.execute(stmt).all()
        # first test
        results = solver.pick_me_donuts_0_1(donuts, 200)
        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 667.80
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 2
        assert results[1] == {12: 1, 13: 1}

        # second test
        results = solver.pick_me_donuts_0_1(donuts, 250)
        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 952.00
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 3
        assert results[1] == {10: 1, 12: 1, 13: 1}


def test_pick_me_donuts_0_1_Grzybki_donuts(app_with_db):
    '''
    test pick me donuts 0 1 - only Grzybki Donuts
    '''
    solver = Solver()
    with app_with_db.app_context():  
        stmt = select(Donuts.id, Donuts.weight, Donuts.kcal)\
                .where(and_(Donuts.manufacturer_id == Manufacturers.id, Manufacturers.name == 'Grzybki'))
        donuts = db.session.execute(stmt).all()

        # first test
        results = solver.pick_me_donuts_0_1(donuts, 200)
        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 813.00
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 2
        assert results[1] == {14: 1, 15: 1}

        # second test
        results = solver.pick_me_donuts_0_1(donuts, 250)
        assert len(results) == 2
        assert type(results[0]) == type(1.5)
        assert round(results[0], 2) == 813.00
        assert type(results[1]) == type(dict())
        assert len(results[1]) == 2
        assert results[1] == {14: 1, 15: 1}
