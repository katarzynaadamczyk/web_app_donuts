'''
test if correct data is in database
if so scraper works correctly
'''
from app.utils import get_all_available_donuts, get_all_available_manufacturers
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
    testing if get_all_available_manufacturers returns 3 manufacturers as in database.json
    '''
    with app_with_db.app_context():
        donuts = get_all_available_donuts()
        assert len(donuts) == 16

