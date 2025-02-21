'''
utils functions

update_database - function returning database
in form of a dict ip_address: sorted_list_of_tags

get_correct_ip_address - function returning correct ip_address
given ip_address in endpoint

'''
from flask import abort, current_app
import ijson
from sqlalchemy import select
import plotly.graph_objects as go
import plotly.utils
import plotly.io as pio
import json
from app.models import *
from app.utils_scraper import Scraper


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
    scraper = Scraper(current_app.db)
    try:
        with open(filename, "rb") as file:
            for item in ijson.items(file, "item"):
                scraper.write_to_db_one_manufacturers_donuts(item)
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def generate_chart(toggle, value):
    '''
    Generates chart based on given parameters.

    Args:
        toggle: bool - True - unlimited algorithm
                       False - 0_1 algorithm
        value: int - how many g of donuts to eat
    
    Returns:
        tuple(dict of fig, int - number of calories)
    '''

    stmt = select(Donuts.id, Donuts.weight, Donuts.kcal)
    with current_app.app_context():
        results = current_app.db.session.execute(stmt).all()
        if toggle:
            result = current_app.solver.pick_me_donuts_unlimited(results, value)
        else:
            result = current_app.solver.pick_me_donuts_0_1(results, value)
        resulting_donuts = current_app.db.session.query(Donuts).filter(Donuts.id.in_(result[1].keys())).all()
        donuts = [d.name for d in resulting_donuts]
        values = list(result[1].values())

    fig = go.Figure(data=[go.Bar(x=donuts, y=values, name="Ilość")])
    fig.update_layout(title="Ilość wybranych pączków", xaxis_title="Rodzaj", yaxis_title="Ilość")

    return fig.to_dict(), round(result[0])

