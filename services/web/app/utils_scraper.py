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
    '''
    class Scraper builds an object to get all needed data
    for project's database
    '''
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

        Args:
            item: dict(str: str/int) {Scraper.LINK: str (link to a web page),
                                      Scraper.NAME: str (name of manufacturer),
                                      Scraper.N: int (Optional, indicates how many subpages to visit)}
        '''
        # add manufacturer to db and get its id
        manufacturer_id = self.add_manufacturer(item[Scraper.NAME])
        
        # get all donuts links
        donuts_links = self.get_all_donuts_links(item)
        
        # add data for given links
        self.add_data_to_db_for_given_links(donuts_links, manufacturer_id)

        return donuts_links
    

    def get_all_donuts_links(self, item):
        '''
        get links to all donuts for given item (manufacturers web page)
        and format them

        Args:
            item: dict(str: str/int) {Scraper.LINK: str (link to a web page),
                                      Scraper.NAME: str (name of manufacturer),
                                      Scraper.N: int (Optional, indicates how many subpages to visit)}
        '''
        donuts_links = []

        # get all links
        if Scraper.N in item.keys():
            donuts_links += self.get_all_donut_pages_with_n_parameter(item)
        else:
            donuts_links += self.get_all_donut_pages_from_given_page(item[Scraper.LINK])
        
        # links formatting
        donuts_links = self.links_formatting(donuts_links, item[Scraper.LINK])
        
        print(donuts_links)
        
        return donuts_links
    

    def links_formatting(self, donuts_links, main_link):
        '''
        function formatting links to be correct

        Args:
            donuts_links: List[str]
            main_link: str (manufacturers web page)
        '''
        if donuts_links and not donuts_links[0].startswith('https://'):
            add_one = 1 if not donuts_links[0].startswith('/') else 0
            add = main_link[0:main_link.find('/', 8) + add_one]
            donuts_links = [add + link for link in donuts_links]
        return donuts_links


    def get_all_donut_pages_with_n_parameter(self, item):
        '''
        get all links to subpages with data about donuts
        when there are subpages on manufacturers web page

        Args:
            item: dict(str: str/int) {Scraper.LINK: str (link to a web page),
                                      Scraper.NAME: str (name of manufacturer),
                                      Scraper.N: int (Optional, indicates how many subpages to visit)} 
        '''
        donut_links = []
        for i in range(1, item[Scraper.N]):
            donut_links += self.get_all_donut_pages_from_given_page(item[Scraper.LINK] + str(i) + '/')
        return donut_links


    def get_all_donut_pages_from_given_page(self, html_link):
        '''
        get all links to subpages with data about donuts

        Args:
            html_link: str (web page html)
        '''
        # get all links having str('paczek') in it (paczek = donut in Polish)
        with self.get_soup(html_link) as soup:
            return [a['href'] for a in soup.find_all('a') if 'paczek' in a['href']]


    @contextmanager
    def get_soup(self, link):
        '''
        context manager returning BeautifulSoup of of given link

        Args:
            link: str (web page html)
        '''
        r = requests.get(link)
        soup = BeautifulSoup(r.text, features="html.parser")
        yield soup



    def add_data_to_db_for_given_links(self, links, manufacturer_id):
        '''
        for each link get data about donut 
        then add all donuts data to db

        Args:
            links: List[str] - list of links of all donuts subpages
            manufacturer_id: int - id of manufacturer for donuts links list
    
        Returns:
            bool: True if all donuts were added to bd, False otherwise
        '''
        # get all donuts data for adding to db
        results = self.get_all_donuts_data(links, manufacturer_id)
        
        # list of values returned by adding donuts to db
        added = []
        
        for item in results:
            added.append(
                self.add_donut(name=item['name'], manufacturer_id=manufacturer_id, kcal=item['kcal'], weight=item['weight'])
                )
            
        return not (len(added) > 0 and None in added)
    

    def get_all_donuts_data(self, links, manufacturer_id):
        '''
        get all data needed to add donuts to db

        Args:
            links: List[str] - list of links of all donuts subpages
            manufacturer_id: int - id of manufacturer for donuts links list

        Returns:
            List[Dict] - Dict contain all data for Donut item
        '''
        results = []
        for link in links:
            with self.get_soup(link) as soup:
                name = self.get_name(soup)
                weight = self.get_weight(soup, name)
                kcal = self.get_kcal(soup, name)
                if name is not None and weight is not None and kcal is not None:
                    kcal = kcal * weight / 100
                    act_dict = {'name': name, 'kcal': kcal, 'weight': weight, 'manufacturer_id': manufacturer_id}
                    print(act_dict)
                    results.append(act_dict)
        return results


    def get_name(self, soup):
        '''
        Gets donut name if possible

        Args:
            soup: BeautifulSoup
    
        Returns:
            name: Optional(str)
        '''
        names = soup.find_all(class_="active")
        names = [name.text for name in names if "pączek" in name.text.lower()]
        if len(names) != 1:
            names = [x.text for x in soup.select('h1')]
        if len(names) == 1:
            name = names[0].strip()
            print('name:', name)
            return name
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
            possible_weights = re.findall(r'\d+\s*g', name)
            if len(possible_weights) == 1:
                weight = int(re.findall(r'\d+', possible_weights[0])[0])
                print('weight:', weight)
                return weight
        elems = [elem for elem in soup.find_all(class_='col-sm-4') \
                    if elem.find_all(string=re.compile(r"\s*" + re.escape(name) + r"\s*"))]
        if elems:
            weights = elems[0].find_all(string=re.compile(r'\d+\s*g'))[0]
            weight = int(re.findall(r'\d+', weights)[0])
            print('weight:', weight)
            return weight
        weights = soup.find_all(string=re.compile(r'\d+,\d+\s*kg'))
        if weights:
            weight = int(float(re.findall(r'\d+,\d+', weights[0])[0].replace(',', '.')) * 1000)
            print('weight:', weight)
            return weight
        return None



    def add_manufacturer(self, name):
        '''
        add manufacturer to db

        Args:
            name: str (name of Manufacturer)
        
        Returns:
            int (manufacturer's id)
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

        Args:
            manufacturer_id: int
            name: str
            kcal: float
            weight: int
        
        Returns:
            Optional(List) List if donut added, None otherwise
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
        return None
    

    def get_kcal(self, soup, name):
        '''
        function to find kcal per 100 g
        
        Args:
            soup: BeautifulSoup
            name: str

        Returns:
            float: kcals per 100 g
        '''
        kcals = []
        for element in soup.find_all(string=re.compile(r'\d+ kcal')):
            kcals.append(element)
        if  0 < len(kcals) < 4:
            value_per_100_g = re.findall(r'\d+ kcal', kcals[0])[0]
        else:
            elem = [elem for elem in soup.find_all(class_='col-sm-4') \
                    if elem.find_all(string=re.compile(r"\s*" + re.escape(name) + r"\s*"))][0]
            value_per_100_g = elem.find_all(string=re.compile(r'\d+ kcal'))[0]
        return int(value_per_100_g[:value_per_100_g.find(' ')])

