from app.utils import get_all_available_manufacturers
import pytest


def test_get_all_available_manufacturers_returns_3_manufacturers(app_with_db):
    '''
    testing if get_correct_ip_address returns a valid ip_address
    '''
    with app_with_db.app_context():
        manufacturers = get_all_available_manufacturers()
        assert len(manufacturers) == 3

    # TODO
    # test for more different ip_addresses