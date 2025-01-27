'''
routes definitions 
'''

from flask import Blueprint, current_app, jsonify, render_template
from markupsafe import Markup
from .utils import get_all_available_donuts

# keep application blueprint
main = Blueprint("main", __name__)


# setting route /
@main.route("/", methods=["GET"]) 
def hello():
    '''
    return JSON for /
    '''
    return jsonify('hello world')


# setting route /some_route_1
@main.route("/listing", methods=["GET"]) 
def some_route_1():
    '''
    return HTML listing available donuts
    '''
    return render_template('donuts_listing.html', donuts=get_all_available_donuts())


# setting route /some_route_2
@main.route("/some_route_2", methods=["GET"]) 
def some_route_2():
    '''
    return JSON for some_route_1
    '''
    return jsonify(task='hi2')

