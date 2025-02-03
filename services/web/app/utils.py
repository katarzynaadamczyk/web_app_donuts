'''
utils functions

update_database - function returning database
in form of a dict ip_address: sorted_list_of_tags

get_correct_ip_address - function returning correct ip_address
given ip_address in endpoint

'''
from bs4 import BeautifulSoup
from contextlib import contextmanager
from flask import abort, current_app
import ijson
import requests
from sqlalchemy import select, and_
import re
from app.models import *

# define json dict keys in case they change over time
LINK = 'html'
NAME = 'name'
N = 'n'


def get_all_available_donuts():
    '''
    returns list of all available in db donuts
    '''
    stmt = select(Donuts.id, Donuts.name, Donuts.weight, Donuts.kcal)
    result = current_app.db.session.execute(stmt).all()
    print(result)
    return result


def get_all_available_manufacturers():
    '''
    returns list of all available in db donuts
    '''
    stmt = select(Manufacturers.id, Manufacturers.name)
    result = current_app.db.session.execute(stmt).all()
    print(result)
    return result


def load_data_from_json(filename):
    '''
    given json filename of available links to manufacturers lists
    of donuts (pastries)
    add all not existing to the database
    '''
    try:
        with open(filename, "rb") as file:
            for item in ijson.items(file, "item"):
                write_to_db_one_manufacturers_donuts(item)
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def write_to_db_one_manufacturers_donuts(item):
    '''
    adds to database all donuts from given webpage to Donuts Table
    and their manufacturer (item[NAME]) to Manufacturers Table
    '''
    manufacturer_id = add_manufacturer(item[NAME])
    donuts_links = []
    if N in item.keys():
        donuts_links += get_all_donut_pages_with_n_parameter(item)
    else:
        donuts_links += get_all_donut_pages_from_given_page(item[LINK])
    if donuts_links and not donuts_links[0].startswith('https://'):
        add_one = 1 if not donuts_links[0].startswith('/') else 0
        add = item[LINK][0:item[LINK].find('/', 8) + add_one]
        donuts_links = [add + link for link in donuts_links]
    print(donuts_links)
    add_data_to_db_for_given_links(donuts_links, manufacturer_id)
    return donuts_links


def get_all_donut_pages_with_n_parameter(item):
    '''
    get all links to subpages with data about donuts 
    '''
    donut_links = []
    for i in range(1, item[N]):
        donut_links += get_all_donut_pages_from_given_page(item[LINK] + str(i) + '/')
    return donut_links


def get_all_donut_pages_from_given_page(html_link):
    '''
    get all links to subpages with data about donuts 
    '''
    with get_soup(html_link) as soup:
        return [a['href'] for a in soup.find_all('a') if 'paczek' in a['href']]


@contextmanager
def get_soup(link):
    '''
    context manager returning BeautifulSoup of of given link
    '''
    r = requests.get(link)
    soup = BeautifulSoup(r.text, features="html.parser")
    yield soup



def add_data_to_db_for_given_links(links, manufacturer_id):
    '''
    for each link get data about donut 
    then add all donuts data to db

    Args:
        links: list[str] - list of links of all donuts subpages
        manufacturer_id: int - id of manufacturer for donuts links list
    
    Returns:
        None - TODO should be True if added, False if not added
    '''
    results = []
    for link in links:
        with get_soup(link) as soup:
            name = get_name(soup)
            weight = get_weight(soup, name)
            kcal = find_kcal(soup)
            if type(kcal) == type(weight) == type(1):
                kcal = kcal * weight / 100
            print('kcal:', kcal)
            if name is not None and weight is not None and kcal is not None:
                act_dict = {'name': name, 'kcal': kcal, 'weight': weight, 'manufacturer_id': manufacturer_id}
                print(act_dict)
                results.append(act_dict)
    for item in results:
        add_donut(name=item['name'], manufacturer_id=manufacturer_id, kcal=item['kcal'], weight=item['weight'])


def get_name(soup):
    '''
    Gets donut name if possible

    Args:
        soup: BeautifulSoup
    
    Returns:
        name: Optional(str)
    '''
    names = soup.find_all(class_="active")
    names = [name for name in names if "pączek" in name.text.lower()]
    if len(names) == 1:
        name = names[0].text.strip()
        print('name:', name)
        return name
    # TODO
    return None


def get_weight(soup, name):
    '''
    Gets donut weight if possible

    Args:
        soup: BeautifulSoup
        name: str (donut name)
    
    Returns:
        weight: Optional(int)
    '''
    if name is not None:
        possible_weights = re.findall(r'\d+ g', name)
        if len(possible_weights) == 1:
            weight = int(re.findall(r'\d+', possible_weights[0])[0])
            print('weight:', weight)
            return weight
    # TODO
    return None



def add_manufacturer(name):
    '''
    add manufacturer to db
    '''
    stmt = select(Manufacturers.id).where(Manufacturers.name == name)
    result = current_app.db.session.execute(stmt).all()
    if len(result) == 0:
        new_item = Manufacturers(
                name=name
            )
        current_app.db.session.add(new_item)
        current_app.db.session.commit()
        print('added', name)
        return current_app.db.session.execute(stmt).all()[0][0]
    return result[0][0]


def add_donut(manufacturer_id, name, kcal, weight):
    '''
    add manufacturer to db
    '''
    stmt = select(Donuts.id).where(
                            and_(
                                Donuts.name == name,
                                Donuts.kcal == kcal,
                                Donuts.manufacturer_id == manufacturer_id,
                                Donuts.weight == weight,
                                )
                            )
    result = current_app.db.session.execute(stmt).all()
    print(result)
    if len(result) == 0:
        new_item = Donuts(
                name=name,
                manufacturer_id=manufacturer_id,
                kcal=kcal,
                weight=weight
            )
        current_app.db.session.add(new_item)
        current_app.db.session.commit()
        print('added', name)
        return current_app.db.session.execute(stmt).all()
    return result
    

def find_kcal(soup):
    '''
    function to find all texts where kcal is in it
    returns kcal per 100 g if len of all kcal appearances is > 0 and < 4
    otherwise
    returns list of all appearances
    '''
    kcals = []
    for element in soup.find_all(text=True):
        for x in re.findall(r'\d+ kcal', element.text):
            kcals.append(element)
    if  0 < len(kcals) < 4:
        value_per_100_g = re.findall(r'\d+ kcal', kcals[0])[0]
        return int(value_per_100_g[:value_per_100_g.find(' ')])

    return None
