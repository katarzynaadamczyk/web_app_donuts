'''
routes definitions 
'''

from flask import Blueprint, current_app, jsonify, render_template
from markupsafe import Markup
from sqlalchemy import select
from .models import Donuts, Manufacturers
from .utils import get_all_available_donuts, get_all_available_manufacturers, load_data_from_json


# keep application blueprint
main = Blueprint("main", __name__)


# setting route /
@main.route("/", methods=["GET"]) 
def hello():
    '''
    return JSON for /
    '''
    return jsonify('hello world')


# setting route /donuts_listing
@main.route("/donuts_listing", methods=["GET"]) 
def donuts_listing():
    '''
    return HTML listing available donuts
    '''
    donuts=get_all_available_donuts()
    return render_template('donuts_listing.html', donuts=donuts)


# setting route /manufacturers_listing
@main.route("/manufacturers_listing", methods=["GET"]) 
def manufacturers_listing():
    '''
    return HTML listing available donuts
    '''
    return render_template('manufacturers_listing.html', lst=get_all_available_manufacturers())


# setting route /solve_all_donuts_infinite
@main.route("/solve_all_donuts_infinite", methods=["GET"]) 
def solve_all_donuts_infinite():
    '''
    return HTML listing top donuts with infinite number of donuts available per 200 g belly
    '''
    stmt = select(Donuts.id, Donuts.weight, Donuts.kcal)
    with current_app.app_context():
        results = current_app.db.session.execute(stmt).all()
        result = current_app.solver.pick_me_donuts_unlimited(results, 200)
    return jsonify(result)


# setting route /solve_all_donuts_0_1
@main.route("/solve_all_donuts_0_1", methods=["GET"]) 
def solve_all_donuts_0_1():
    '''
    return HTML listing top donuts with 0 1 algorithm per 200 g belly
    '''
    stmt = select(Donuts.id, Donuts.weight, Donuts.kcal)
    with current_app.app_context():
        results = current_app.db.session.execute(stmt).all()
        result = current_app.solver.pick_me_donuts_0_1(results, 200)
    return jsonify(result)


# setting route /some_route_2
@main.route("/test", methods=["GET"]) 
def some_route_2():
    '''
    return JSON for rest
    '''
    return jsonify(json='hello')

