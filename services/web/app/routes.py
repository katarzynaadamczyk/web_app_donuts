'''
routes definitions 
'''

from flask import Blueprint, current_app, jsonify, render_template, request
import numpy as np
from sqlalchemy import select
from .models import Donuts, Manufacturers
from .utils import generate_chart, get_all_available_donuts, get_all_available_manufacturers


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


# setting route /test_2
@main.route("/donuts_to_eat", methods=["GET"]) 
def donuts_to_eat():
    '''
    return JSON for rest
    '''
    return render_template("visualization2.html")


@main.route("/update_chart", methods=["POST"])
def update_chart():
    data = request.get_json()
    toggle = data.get("toggle", False)
    slider_value = int(data.get("slider", 50))

    new_chart, kcal = generate_chart(toggle, slider_value)

    return jsonify(data=new_chart, dynamic_value=kcal)

