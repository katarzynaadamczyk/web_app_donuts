'''
class to get data from web pages

'''

from bs4 import BeautifulSoup
from contextlib import contextmanager
import requests
from sqlalchemy import select, and_
import re
from app.models import *

class Scraper:
    # define json dict keys in case they change over time
    LINK = 'html'
    NAME = 'name'
    N = 'n'

    def __init__(self, db):
        '''
        Initialize scraper object by assigning db to it

        Args:
            db: SQLAlchemy
        '''
        self.db = db


    def write_to_db_one_manufacturers_donuts(self, item):
        '''
        adds to database all donuts from given webpage to Donuts Table
        and their manufacturer (item[NAME]) to Manufacturers Table
        '''
        manufacturer_id = self.add_manufacturer(item[Scraper.NAME])
        donuts_links = []
        if Scraper.N in item.keys():
            donuts_links += self.get_all_donut_pages_with_n_parameter(item)
        else:
            donuts_links += self.get_all_donut_pages_from_given_page(item[Scraper.LINK])
        if donuts_links and not donuts_links[0].startswith('https://'):
            add_one = 1 if not donuts_links[0].startswith('/') else 0
            add = item[Scraper.LINK][0:item[Scraper.LINK].find('/', 8) + add_one]
            donuts_links = [add + link for link in donuts_links]
        print(donuts_links)
        self.add_data_to_db_for_given_links(donuts_links, manufacturer_id)
        return donuts_links


    def get_all_donut_pages_with_n_parameter(self, item):
        '''
        get all links to subpages with data about donuts 
        '''
        donut_links = []
        for i in range(1, item[Scraper.N]):
            donut_links += self.get_all_donut_pages_from_given_page(item[Scraper.LINK] + str(i) + '/')
        return donut_links


    def get_all_donut_pages_from_given_page(self, html_link):
        '''
        get all links to subpages with data about donuts 
        '''
        with self.get_soup(html_link) as soup:
            return [a['href'] for a in soup.find_all('a') if 'paczek' in a['href']]


    @contextmanager
    def get_soup(self, link):
        '''
        context manager returning BeautifulSoup of of given link
        '''
        r = requests.get(link)
        soup = BeautifulSoup(r.text, features="html.parser")
        yield soup



    def add_data_to_db_for_given_links(self, links, manufacturer_id):
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
            with self.get_soup(link) as soup:
                name = self.get_name(soup)
                weight = self.get_weight(soup, name)
                kcal = self.get_kcal(soup)
                if type(kcal) == type(weight) == type(1):
                    kcal = kcal * weight / 100
                print('kcal:', kcal)
                if name is not None and weight is not None and kcal is not None:
                    act_dict = {'name': name, 'kcal': kcal, 'weight': weight, 'manufacturer_id': manufacturer_id}
                    print(act_dict)
                    results.append(act_dict)
        for item in results:
            self.add_donut(name=item['name'], manufacturer_id=manufacturer_id, kcal=item['kcal'], weight=item['weight'])


    def get_name(self, soup):
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


    def get_weight(self, soup, name):
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



    def add_manufacturer(self, name):
        '''
        add manufacturer to db
        '''
        stmt = select(Manufacturers.id).where(Manufacturers.name == name)
        result = self.db.session.execute(stmt).all()
        if len(result) == 0:
            new_item = Manufacturers(
                    name=name
                )
            self.db.session.add(new_item)
            self.db.session.commit()
            print('added', name)
            return self.db.session.execute(stmt).all()[0][0]
        return result[0][0]


    def add_donut(self, manufacturer_id, name, kcal, weight):
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
        result = self.db.session.execute(stmt).all()
        print(result)
        if len(result) == 0:
            new_item = Donuts(
                    name=name,
                    manufacturer_id=manufacturer_id,
                    kcal=kcal,
                    weight=weight
                )
            self.db.session.add(new_item)
            self.db.session.commit()
            print('added', name)
            return self.db.session.execute(stmt).all()
        return result
    

    def get_kcal(self, soup):
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