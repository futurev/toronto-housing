from app import app
from flask import render_template

from flask import flash, Blueprint, request, redirect, render_template, url_for
from flask import jsonify, Markup, send_from_directory, Response, make_response
from flask.views import MethodView
import json
import os
import requests
from random import randint
import csv
import re
from jinja2 import Environment, FileSystemLoader

from app import database_operations as dbo
from app import config

BG_data = Blueprint('BG_data', __name__, template_folder='templates')
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

env = Environment(loader=FileSystemLoader(config.QUERIES_PATH))

class Splash(MethodView):
    # decorators = [login_required]
    def get(self):
        return render_template('splash.html')

class Home(MethodView):
    # decorators = [login_required]
    def get(self):
        return render_template('home.html')

class Explore(MethodView):
    # decorators = [login_required]
    def get(self):
        return render_template('explore.html')

BG_data.add_url_rule('/', view_func=Splash.as_view('Splash'))
BG_data.add_url_rule('/home', view_func=Home.as_view('Home'))
BG_data.add_url_rule('/explore', view_func=Explore.as_view('Explore'))



@app.route('/get_config')
def get_config():
    json_path = os.path.join(ROOT_PATH, 'toronto-housing/app/static/main_config.json')
    print json_path
    with open(json_path) as data_file:
        data = json.load(data_file)
    response = jsonify(results=data)
    return response

##TODO: document everything!
##TODO: split out some of htese functions into classes/separate modules



def queryDB(query_file, params, cols=False, cols_format='dict'):
    conn = dbo.getConnection()
    sql_template = env.get_template(query_file)
    query = sql_template.render(params)
    data = dbo.query(conn, query, cols=cols, cols_format=cols_format)
    return data

@app.route('/fsa_api')
def fsa_api():
    province = request.args.get('province')
    params = {'province_filter': "'{}'".format(province)}

    print ('querying db for fsa data')
    data = queryDB('fsa.sql', params, True)
    print ('query returned %s rows' % len(data))

    fsa_list = []
    property_keys = ['fsa','province','stat']
    for row in data:
        properties_dict = {key:row[key] for key in property_keys}
        fsa_data = dict(geometry=eval(row['geom']), type='Feature')

        fsa_data['properties'] = properties_dict
        fsa_list.append(fsa_data)

    return jsonify(type='FeatureCollection', features=fsa_list)
