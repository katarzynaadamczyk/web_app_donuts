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
from sqlalchemy import select
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
    add_manufacturer(item[NAME])
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
    add_data_to_db_for_given_links(donuts_links)
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



def add_data_to_db_for_given_links(links):
    '''
    get all links to subpages with data about donuts 
    '''
    for link in links:
        with get_soup(link) as soup:
            names = soup.find_all(class_="active")
            #names = soup.find_all('title') # (string=lambda text: 'active' in text.lower())
            names = [name for name in names if "pączek" in name.text.lower()]
            if len(names) == 1:
                name = names[0].text
                print('name:', name)
                print(re.findall(r'\d+ g', name))
                if ' g' in name:
                    weight = int(re.findall(r'\d+', name)[0])
                    print('weight:', weight)
            else:
                print('not one name')
                for name in names:
                    print('name:', name.text.strip())
            print(find_kcal(soup))
    #    kcal_index = kcal_numbers.find(' kcal')
     #   kcal = float(kcal_numbers[:kcal_index-1].rfind(' '))
        


     #   elementy = soup.find_all(text=re.compile(r"\d+")) # szukanie liczb
     #   for element in elementy:
      #      print(element.strip())
      #  break
    # TODO
    pass
  #  r = requests.get(html_link)
   # soup = BeautifulSoup(r.text, features="html.parser")
  #  return [a['href'] for a in soup.find_all('a') if 'paczek' in a['href']]


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
        return current_app.db.session.execute(stmt).all()[0]
    return False


def add_donut(manufacturer_id, name, kcal, weight):
    '''
    add manufacturer to db
    '''
    stmt = select(Donuts.id).where(Donuts.name == name).where(Donuts.kcal == kcal)\
           .where(Donuts.manufacturer_id == manufacturer_id).where(Donuts.weight == weight)
    result = current_app.db.session.execute(stmt).all()
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
        return current_app.db.session.execute(stmt).all()[0]
    return False
    

def find_kcal(soup):
    liczby = []
    for element in soup.find_all(text=True):
        for x in re.findall(r'\d+ kcal', element.text):
            liczby.append(element)

    return liczby
