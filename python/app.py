#!/usr/bin/python3

from flask import Flask, render_template, jsonify, request
from random import sample
import json
import time
import collections
import database

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('chart.html')
            
@app.route('/data')
def data():
    return jsonify(database.get_averages())
            
@app.route('/add', methods=['POST'])
def add_data():
    post_data = json.loads(request.data.decode("utf-8"))
    parse_data(post_data)
    return jsonify({"hi": 3})

def parse_data(data):
    if isinstance(data, dict):
        try:
            app.logger.debug(data)
            database.insert_database(temperature=float(data['temperature']), temperature2=float(data['temperature2']), humidity=float(data['humidity']), pressure=float(data['pressure']), altitude=float(data['altitude']), light=float(data['light']))
        except KeyError:
            app.logger.error('Failed to find key in JSON')
    else:
        return None

if __name__ == '__main__':
    database.create_database()
    app.run(debug=True, host='0.0.0.0')
