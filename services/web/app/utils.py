'''
utils functions

update_database - function returning database
in form of a dict ip_address: sorted_list_of_tags

get_correct_ip_address - function returning correct ip_address
given ip_address in endpoint

'''
from bs4 import BeautifulSoup
from flask import abort, current_app
import requests
from sqlalchemy import select
from app.models import *


def get_all_available_donuts():
    '''
    returns list of all available in db donuts
    '''
    stmt = select(Donuts.id, Donuts.name, Donuts.weight, Donuts.kcal)
    result = current_app.db.session.execute(stmt).all()
    return result


def get_all_available_manufacturers():
    '''
    returns list of all available in db donuts
    '''
    stmt = select(Manufacturers.id, Manufacturers.name)
    result = current_app.db.session.execute(stmt).all()
    return result


def get_all_one_manufacturer_donuts():
    '''
    adds to database all donuts from given webpage
    '''
    web_url = 'https://www.putka.pl/produkty/8/bulki-slodkie/'
    web_url_2 = 'https://www.oskroba.pl/produkty/pieczywo-codzienne/paczki-drozdzowki'
    a_paczek = []
    for i in range(1, 10):
        r = requests.get(web_url + str(i) + '//')
        soup = BeautifulSoup(r.text)
        new_a_paczek = [a['href'] for a in soup.find_all('a') if 'paczek' in a['href']]
        a_paczek += new_a_paczek
    return a_paczek
