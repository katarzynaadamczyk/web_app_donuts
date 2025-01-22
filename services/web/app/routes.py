'''
routes definitions 
'''

from flask import Blueprint, current_app, jsonify, render_template
from markupsafe import Markup

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
@main.route("/some_route_1", methods=["GET"]) 
def some_route_1(value):
    '''
    return JSON for some_route_1
    '''
    return jsonify(task='hi')


# setting route /some_route_2
@main.route("/some_route_2", methods=["GET"]) 
def get_ip_tags_report(value):
    '''
    return JSON for some_route_1
    '''
    return jsonify(task='hi2')

