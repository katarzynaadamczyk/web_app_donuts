'''
routes definitions 
'''

from flask import Blueprint, current_app, jsonify, render_template, request
import numpy as np
from sqlalchemy import select
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import plotly.io as pio
import json
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

# setting route /solve_all_donuts_infinite_2
@main.route("/solve_all_donuts_infinite_2/<value>", methods=["GET"]) 
def solve_all_donuts_infinite_2(value):
    '''
    return HTML listing top donuts with infinite number of donuts available per 200 g belly
    '''
    try:
        value = int(value)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    pio.renderers.default = "browser"
    stmt = select(Donuts.id, Donuts.weight, Donuts.kcal)
    with current_app.app_context():
        results = current_app.db.session.execute(stmt).all()
        result = current_app.solver.pick_me_donuts_unlimited(results, value)
        resulting_donuts = current_app.db.session.query(Donuts).filter(Donuts.id.in_(result[1].keys())).all()
        donuts = [d.name for d in resulting_donuts]
        values = list(result[1].values())
    
    print(result)
    
    fig = go.Figure(data=[go.Bar(x=donuts , y=values)])
    fig.update_yaxes(type='linear')

    print(fig)
    print(fig.data[0]['y'])
    # Konwersja wykresu do JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("visualization.html", graphJSON=graphJSON, kcal=round(result[0], 2))

# setting route /test_2
@main.route("/test_2", methods=["GET"]) 
def test_2():
    '''
    return JSON for rest
    '''
    return render_template("visualization2.html")


def generate_chart(toggle, value):
    """Tworzy wykres w zależności od parametrów."""

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


@main.route("/update_chart", methods=["POST"])
def update_chart():
    data = request.get_json()
    toggle = data.get("toggle", False)
    slider_value = int(data.get("slider", 50))

    new_chart, kcal = generate_chart(toggle, slider_value)

    return jsonify(data=new_chart, dynamic_value=kcal)

